import json
import logging
from math import radians, cos, sin, asin, sqrt

import requests

logger = logging.getLogger('gios_api')
logger.setLevel(logging.INFO)


class GiosApi:
    address = 'http://api.gios.gov.pl/pjp-api/rest'

    @classmethod
    def get_stations(cls):
        """
        Stacje pomiarowe
        Usługa sieciowa udostępniająca listę stacji pomiarowych.
        http://api.gios.gov.pl/pjp-api/rest/station/findAll

        Usługa sieciowa typu REST wykorzystująca zapytanie HTTP GET. Udostępniająca dane w formacie JSON.

        Przykład zapytania: Usługa nie przyjmuje parametrów wejściowych.

        Przykład odpowiedzi:

        [{
            "id": 14,
            "stationName": "Działoszyn",
            "gegrLat": "50.972167",
            "gegrLon": "14.941319",
            "city": {
                "id": 192,
                "name": "Działoszyn",
                "commune": {
                    "communeName": "Bogatynia",
                    "districtName": "zgorzelecki",
                    "provinceName": "DOLNOŚLĄSKIE"
                }
            },
            "addressStreet": null
        }]
        """
        return cls.get_response('/station/findAll')

    @classmethod
    def get_devices(cls, station_id):
        """
        Stanowiska pomiarowe
        Usługa sieciowa udostępniająca listę stanowisk pomiarowych dostępnych na wybranej stacji pomiarowej.
        http://api.gios.gov.pl/pjp-api/rest/station/sensors/{stationId}

        Usługa sieciowa typu REST wykorzystująca zapytanie HTTP GET. Udostępniająca dane w formacie JSON.

        Przykład zapytania: http://api.gios.gov.pl/pjp-api/rest/station/sensors/14

        Przykład odpowiedzi:

        [{
            "id": 92,
            "stationId": 14,
            "param": {
                "paramName": "pył zawieszony PM10",
                "paramFormula": "PM10",
                "paramCode": "PM10",
                "idParam": 3
            }
        },
        {
            "id": 88,
            "stationId": 14,
            "param": {
                "paramName": "dwutlenek azotu",
                "paramFormula": "NO2",
                "paramCode": "NO2",
                "idParam": 6
            }
        }]
        """
        return cls.get_response('/station/sensors/' + station_id)

    @classmethod
    def get_measurment(cls, device_id):
        """
        Dane pomiarowe
        Usługa sieciowa udostępniająca dane pomiarowe na podstawie podanego identyfikatora stanowiska pomiarowego.
        http://api.gios.gov.pl/pjp-api/rest/data/getData/{sensorId}

        Usługa sieciowa typu REST wykorzystująca zapytanie HTTP GET. Udostępniająca dane w formacie JSON.

        Przykład zapytania: http://api.gios.gov.pl/pjp-api/rest/data/getData/92

        Przykład odpowiedzi:

        {
            "key": "PM10",
            "values": [
            {
                "date": "2017-03-28 11:00:00",
                "value": 30.3018
            },
            {
                "date": "2017-03-28 12:00:00",
                "value": 27.5946
            }]
        }
        """
        return cls.get_response('/data/getData/' + device_id)

    @classmethod
    def get_air_index(cls, station_id):
        """
        Indeks jakości powietrza
        Usługa sieciowa udostępniająca indeks jakości powietrza na podstawie podanego identyfikatora stacji pomiarowej.
        http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/{stationId}

        Usługa sieciowa typu REST wykorzystująca zapytanie HTTP GET. Udostępniająca dane w formacie JSON.

        Przykład zapytania: http://api.gios.gov.pl/pjp-api/rest/aqindex/getIndex/52

        Przykład odpowiedzi:

        {
            "id": 52,
            "stCalcDate": "2017-03-28 12:00:00",
            "stIndexLevel": {
                "id": 2,
                "indexLevelName": "Umiarkowany"
            },
            "stSourceDataDate": "2017-03-28 12:00:00",
            "so2CalcDate": "2017-03-28 12:00:00",
            "so2IndexLevel": null,
            "so2SourceDataDate": "2017-03-28 12:00:00",
            "no2CalcDate": "2017-03-28 12:00:00",
            "no2IndexLevel": null,
            "no2SourceDataDate": "2017-03-28 12:00:00",
            "coCalcDate": "2017-03-28 12:00:00",
            "coIndexLevel": null,
            "coSourceDataDate": "2017-03-28 12:00:00",
            "pm10CalcDate": "2017-03-28 12:00:00",
            "pm10IndexLevel": null,
            "pm10SourceDataDate": "2017-03-28 12:00:00",
            "pm25CalcDate": "2017-03-28 12:00:00",
            "pm25IndexLevel": null,
            "pm25SourceDataDate": null,
            "o3CalcDate": "2017-03-28 12:00:00",
            "o3IndexLevel": null,
            "o3SourceDataDate": "2017-03-28 12:00:00",
            "c6h6CalcDate": "2017-03-28 12:00:00",
            "c6h6IndexLevel": null,
            "c6h6SourceDataDate": "2017-03-28 12:00:00"
        }
        """
        return cls.get_response('/aqindex/getIndex/' + str(station_id))

    @classmethod
    def get_response(cls, endpoint):
        address = cls.address + endpoint
        logger.info(address + " GET")
        response = requests.get(address)
        if response.status_code == 200:
            logger.info('200')
            return response.text
        if response.status_code == 404:
            logger.warning('404')
            raise FileNotFoundError
        else:
            msg = 'GIOS API unknown error! Http error: %s' % response.status_code
            logger.error(msg)
            raise ConnectionError(msg)


class GiosService:
    @classmethod
    def get_nearest_station_data(cls, lat, lon):  # TODO: unit testy
        nearest = cls.get_nearest_station(lat, lon)
        data = json.loads(GiosApi.get_air_index(nearest['id']))
        payload = {'stataion': nearest, 'data': data}
        return payload

    @classmethod
    def get_nearest_station(cls, lat, lon):  # TODO: unit testy
        logger.info('Get nearest lat=%s, lon=%s' % (lat, lon))
        stations = json.loads(GiosApi.get_stations())
        nearest = None
        for station in stations:
            station['distance'] = cls.calculate_distance(lat, lon, station['gegrLat'], station['gegrLon'])
            if not nearest or nearest.get('distance') > station.get('distance'):
                nearest = station
        logger.info('Nearest id=%s' % nearest['id'])
        return nearest

    @classmethod
    def calculate_distance(cls, lat1, lon1, lat2, lon2):
        """https://www.geeksforgeeks.org/program-distance-two-points-earth/"""

        # The math module contains a function named
        # radians which converts from degrees to radians.
        lon1 = radians(float(lon1))
        lon2 = radians(float(lon2))
        lat1 = radians(float(lat1))
        lat2 = radians(float(lat2))

        # Haversine formula #TODO: sprawdzić czy to poprawna metoda obliczania
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

        c = 2 * asin(sqrt(a))

        # Radius of earth in kilometers. Use 3956 for miles
        r = 6371

        # calculate the result
        return c * r
