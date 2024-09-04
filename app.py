from flask import Flask, request, jsonify
import requests
from cachetools import TTLCache
import csv

app = Flask(__name__)

GEOCODING_API_URL = "http://api.openweathermap.org/geo/1.0/direct"
GEOCODING_API_ZIP_URL = "http://api.openweathermap.org/geo/1.0/zip"
GEOCODING_API_KEY = "9bdf4a798991a53dd53450033c37ea70"
LOCODE_DATA_URL = "https://raw.githubusercontent.com/datasets/un-locode/master/data/code-list.csv"

cache = TTLCache(maxsize=100, ttl=600)
locode_cache = {}

def load_locode_data():
    global locode_cache
    try:
        response = requests.get(LOCODE_DATA_URL)
        response.raise_for_status()
        locode_data = csv.reader(response.text.splitlines())
        next(locode_data)
        for row in locode_data:
            if len(row) < 3:
                continue
            country_code = row[1].strip()
            location_code = row[2].strip()
            full_locode = f"{country_code} {location_code}"
            locode_cache[full_locode] = {
                "city": row[3].strip(),
                "state": row[5].strip() if len(row) > 5 and row[5] else "",
                "country": country_code
            }
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error loading LOCODE data: {e}")

load_locode_data()
session = requests.Session()

def get_coordinates_from_address(city, state, country):
    cache_key = f"{city},{state},{country}"
    if cache_key in cache:
        return cache[cache_key]

    params = {
        "q": f"{city},{state},{country}",
        "limit": 1,
        "appid": GEOCODING_API_KEY
    }
    try:
        response = session.get(GEOCODING_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if not data or not isinstance(data, list) or len(data) == 0:
            return None

        coordinates = {"latitude": data[0]["lat"], "longitude": data[0]["lon"]}
        cache[cache_key] = coordinates
        return coordinates
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching coordinates for address: {e}")
        return None

def get_coordinates_from_zip(zip_code, country):
    cache_key = f"{zip_code},{country}"
    if cache_key in cache:
        return cache[cache_key]

    params = {
        "zip": f"{zip_code},{country}",
        "appid": GEOCODING_API_KEY
    }
    try:
        response = session.get(GEOCODING_API_ZIP_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if 'lat' in data and 'lon' in data:
            coordinates = {"latitude": data["lat"], "longitude": data["lon"]}
            cache[cache_key] = coordinates
            return coordinates
        return None
    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error fetching coordinates for ZIP code: {e}")
        return None

def get_address_from_locode(locode):
    return locode_cache.get(locode)

@app.route('/geocode', methods=['POST'])
def geocode():
    try:
        data = request.get_json(force=True, silent=True)
        if data is None:
            return jsonify({"error": "Invalid request format"}), 400
        if "zip" in data and "country" in data:
            coordinates = get_coordinates_from_zip(data["zip"], data["country"])
            if coordinates:
                return jsonify(coordinates), 200
            else:
                return jsonify({"error": "Location not found"}), 404
        elif "city" in data and "state" in data and "country" in data:
            coordinates = get_coordinates_from_address(data["city"], data["state"], data["country"])
            if coordinates:
                return jsonify(coordinates), 200
            else:
                return jsonify({"error": "Location not found"}), 404
        elif "locode" in data:
            address = get_address_from_locode(data["locode"])
            if address:
                coordinates = get_coordinates_from_address(address["city"], address["state"], address["country"])
                if coordinates:
                    return jsonify(coordinates), 200
                else:
                    return jsonify({"error": "Location not found"}), 404
            else:
                return jsonify({"error": "Locode not found"}), 404

        return jsonify({"error": "Invalid request format"}), 400

    except Exception as e:
        app.logger.error(f"Unhandled error: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(400)
def bad_request_error(error):
    return jsonify({"error": "Invalid request format"}), 400

@app.errorhandler(404)
def not_found_error(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)

