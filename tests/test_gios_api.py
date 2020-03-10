from unittest import TestCase

from app.gios_api import GiosService


class TestGiosService(TestCase):
    def test_calculate_distance_lat_lon_are_numbers(self):
        lat1 = 53.32055555555556
        lat2 = 53.31861111111111
        lon1 = -1.7297222222222221
        lon2 = -1.6997222222222223

        self.assertEqual(2.0043678382716137, GiosService.calculate_distance(lat1, lon1, lat2, lon2))

    def test_calculate_distance_lat_lon_are_strings(self):
        lat1 = '53.32055555555556'
        lat2 = '53.31861111111111'
        lon1 = '-1.7297222222222221'
        lon2 = '-1.6997222222222223'

        self.assertEqual(2.0043678382716137, GiosService.calculate_distance(lat1, lon1, lat2, lon2))

    def test_calculate_distance_lat_lon_are_equal(self):
        lat1 = '53.32055555555556'
        lat2 = 53.32055555555556
        lon1 = '-1.7297222222222221'
        lon2 = -1.7297222222222221

        self.assertEqual(0, GiosService.calculate_distance(lat1, lon1, lat2, lon2))
