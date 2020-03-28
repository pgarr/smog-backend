from app.gios_api import GiosService


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
