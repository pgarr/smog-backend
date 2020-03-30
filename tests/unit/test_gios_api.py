# -*- encoding: utf-8 -*-
import json

import pytest
import requests

from app.gios_api import GiosService, GiosApi

station1 = {"id": 114, "stationName": "Wrocław - Bartnicza", "gegrLat": "51.111111", "gegrLon": "17.111111"}
station2 = {"id": 117, "stationName": "Wrocław - Korzeniowskiego", "gegrLat": "51.111112", "gegrLon": "17.111112"}
station3 = {"id": 129, "stationName": "Wrocław - Wiśniowa", "gegrLat": "51.211111", "gegrLon": "17.211111"}
station4 = {"id": 52, "stationName": "Legnica - Rzeczypospolitej", "gegrLat": "51.5", "gegrLon": "17.5"}
station5 = {"id": 109, "stationName": "Wałbrzych - Wysockiego", "gegrLat": "52", "gegrLon": "18"}

air_index = {
    "id": 530, "stCalcDate": "2020-03-30 17:35:18", "stIndexLevel": {"id": 1, "indexLevelName": "Dobry"},
    "stSourceDataDate": "2020-03-30 16:00:00",
    "so2CalcDate": "2020-03-30 17:35:18", "so2IndexLevel": None, "so2SourceDataDate": None,
    "no2CalcDate": "2020-03-30 17:35:18", "no2IndexLevel": {"id": 1, "indexLevelName": "Dobry"},
    "no2SourceDataDate": "2020-03-30 16:00:00",
    "coCalcDate": "2020-03-30 17:35:18", "coIndexLevel": {"id": 0, "indexLevelName": "Bardzo dobry"},
    "coSourceDataDate": "2020-03-30 16:00:00",
    "pm10CalcDate": "2020-03-30 17:35:18", "pm10IndexLevel": {"id": 0, "indexLevelName": "Bardzo dobry"},
    "pm10SourceDataDate": "2020-03-30 16:00:00",
    "pm25CalcDate": "2020-03-30 17:35:18", "pm25IndexLevel": {"id": 0, "indexLevelName": "Bardzo dobry"},
    "pm25SourceDataDate": "2020-03-30 16:00:00",
    "o3CalcDate": None, "o3IndexLevel": None, "o3SourceDataDate": None,
    "c6h6CalcDate": "2020-03-30 17:35:18", "c6h6IndexLevel": {"id": 0, "indexLevelName": "Bardzo dobry"},
    "c6h6SourceDataDate": "2020-03-30 16:00:00",
    "stIndexStatus": True, "stIndexCrParam": "OZON"
}


class MockGiosApi:
    @classmethod
    def get_stations(cls):
        return json.dumps([station1, station2, station3, station4, station5])

    @classmethod
    def get_devices(cls, station_id):
        return "mock"

    @classmethod
    def get_measurement(cls, device_id):
        return "mock"

    @classmethod
    def get_air_index(cls, station_id):
        return json.dumps(air_index)


@pytest.fixture(autouse=True)
def mock_giosapi(monkeypatch):
    monkeypatch.setattr(GiosApi, 'get_stations', MockGiosApi.get_stations)
    monkeypatch.setattr(GiosApi, 'get_devices', MockGiosApi.get_devices)
    monkeypatch.setattr(GiosApi, 'get_measurement', MockGiosApi.get_measurement)
    monkeypatch.setattr(GiosApi, 'get_air_index', MockGiosApi.get_air_index)


@pytest.fixture
def mock_response200(monkeypatch):
    class MockResponse200:
        status_code = 200
        text = "Great!"

    def mock_get(*args, **kwargs):
        return MockResponse200()

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_response404(monkeypatch):
    class MockResponse404:
        status_code = 404

    def mock_get(*args, **kwargs):
        return MockResponse404()

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_response500(monkeypatch):
    class MockResponse500:
        status_code = 500

    def mock_get(*args, **kwargs):
        return MockResponse500()

    monkeypatch.setattr(requests, "get", mock_get)


def test_get_response_when_200(mock_response200):
    assert GiosApi.get_response("test") == "Great!"


def test_get_response_when_404(mock_response404):
    with pytest.raises(FileNotFoundError):
        response = GiosApi.get_response("test")


def test_get_response_when_500(mock_response500):
    with pytest.raises(ConnectionError) as excinfo:
        GiosApi.get_response("test")
    assert "Http error: 500" in str(excinfo.value)


def test_calculate_distance_lat_lon_are_numbers():
    lat1 = 53.32055555555556
    lat2 = 53.31861111111111
    lon1 = -1.7297222222222221
    lon2 = -1.6997222222222223

    assert GiosService.calculate_distance(lat1, lon1, lat2, lon2) == 2.0043678382716137


def test_calculate_distance_lat_lon_are_strings():
    lat1 = '53.32055555555556'
    lat2 = '53.31861111111111'
    lon1 = '-1.7297222222222221'
    lon2 = '-1.6997222222222223'

    assert GiosService.calculate_distance(lat1, lon1, lat2, lon2) == 2.0043678382716137


def test_calculate_distance_lat_lon_are_equal():
    lat1 = '53.32055555555556'
    lat2 = 53.32055555555556
    lon1 = '-1.7297222222222221'
    lon2 = -1.7297222222222221

    assert GiosService.calculate_distance(lat1, lon1, lat2, lon2) == 0


def test_get_nearest_station_latlon_equals_to_station():
    lat = station2.get("gegrLat")
    lon = station2.get("gegrLon")
    name = station2.get("stationName")
    nearest = GiosService.get_nearest_station(lat, lon)
    assert nearest["distance"] == 0
    assert nearest["stationName"] == name


def test_get_nearest_station_latlon_higher_then_highest():
    lat = float(station5.get("gegrLat")) + 0.0001
    lon = float(station5.get("gegrLon")) + 0.0001
    name = station5.get("stationName")
    nearest = GiosService.get_nearest_station(lat, lon)
    assert nearest["stationName"] == name


def test_get_nearest_station_latlon_lower_then_lowest():
    lat = float(station1.get("gegrLat")) - 0.0001
    lon = float(station1.get("gegrLon")) - 0.0001
    name = station1.get("stationName")
    nearest = GiosService.get_nearest_station(lat, lon)
    assert nearest["stationName"] == name
