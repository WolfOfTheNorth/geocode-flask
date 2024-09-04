import unittest
from app import app

class GeocodeAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # TEST 1: Test the geocode endpoint with valid city, state, zip, and country
    def test_geocode_with_valid_city_state_zip_country(self):
        response = self.app.post('/geocode', json={
            "city": "Montreal",
            "state": "QC",
            "zip": "H9A",
            "country": "CA"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("latitude", data)
        self.assertIn("longitude", data)
        self.assertIsInstance(data["latitude"], float)
        self.assertIsInstance(data["longitude"], float)

    # TEST 2: Test the geocode endpoint with an invalid city
    def test_geocode_with_invalid_city(self):
        response = self.app.post('/geocode', json={
            "city": "InvalidCityName",
            "state": "QC",
            "country": "CA"
        })
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["error"], "Location not found")

    # TEST 3: Test the geocode endpoint with a valid locode
    def test_geocode_with_valid_locode(self):
        response = self.app.post('/geocode', json={
            "locode": "CA MTR"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("latitude", data)
        self.assertIn("longitude", data)
        self.assertIsInstance(data["latitude"], float)
        self.assertIsInstance(data["longitude"], float)

    # TEST 4: Test the geocode endpoint with an invalid locode
    def test_geocode_with_invalid_locode(self):
        response = self.app.post('/geocode', json={
            "locode": "XX XXX"
        })
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["error"], "Locode not found")

    # TEST 5: Test the geocode endpoint with missing city field
    def test_geocode_with_missing_city_and_zip(self):
        response = self.app.post('/geocode', json={
            "state": "QC",
            "country": "CA"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["error"], "Invalid request format")

    # TEST 6: Test the geocode endpoint with missing country field
    def test_geocode_with_missing_country(self):
        response = self.app.post('/geocode', json={
            "city": "Montreal",
            "state": "QC",
            "zip": "H9A"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["error"], "Invalid request format")

    # TEST 7: Test the geocode endpoint with special characters in the city name
    def test_geocode_with_special_characters_in_city(self):
        response = self.app.post('/geocode', json={
            "city": "Montréal",
            "state": "QC",
            "zip": "H9A",
            "country": "CA"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("latitude", data)
        self.assertIn("longitude", data)
        self.assertIsInstance(data["latitude"], float)
        self.assertIsInstance(data["longitude"], float)

    # TEST 8: Test the geocode endpoint with a very long city name
    def test_geocode_with_very_long_city_name(self):
        long_city_name = "A" * 256  # 256 characters long
        response = self.app.post('/geocode', json={
            "city": long_city_name,
            "state": "QC",
            "country": "CA"
        })
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["error"], "Location not found")

    # TEST 9: Test the geocode endpoint with numeric values in city field
    def test_geocode_with_numeric_city(self):
        response = self.app.post('/geocode', json={
            "city": "12345",
            "state": "QC",
            "country": "CA"
        })
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["error"], "Location not found")

    # TEST 10: Test the geocode endpoint with invalid JSON structure
    def test_geocode_with_invalid_json(self):
        response = self.app.post('/geocode', data='{"city": "Montreal", "state": "QC"', content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["error"], "Invalid request format")

    # TEST 11: Test the geocode endpoint with an empty JSON body
    def test_geocode_with_empty_json(self):
        response = self.app.post('/geocode', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data["error"], "Invalid request format")

    # TEST 12: Test the geocode endpoint with only zip and country
    def test_geocode_with_zip_and_country_only(self):
        response = self.app.post('/geocode', json={
            "zip": "90210",
            "country": "US"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn("latitude", data)
        self.assertIn("longitude", data)
        self.assertIsInstance(data["latitude"], float)
        self.assertIsInstance(data["longitude"], float)

    # TEST 13: Test the geocode endpoint with invalid ZIP code
    def test_geocode_with_invalid_zip(self):
        response = self.app.post('/geocode', json={
            "zip": "00000",
            "country": "US"
        })
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["error"], "Location not found")

    # TEST 14: Test the geocode endpoint with ZIP code and special characters in country code
    def test_geocode_with_special_characters_in_country(self):
        response = self.app.post('/geocode', json={
            "zip": "90210",
            "country": "@U$"
        })
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data["error"], "Location not found")

if __name__ == '__main__':
    unittest.main()
