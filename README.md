# Geocode HTTP Server

This project implements a simple HTTP server using Flask that accepts POST requests at the `/geocode` endpoint. The server can handle two types of requests: one that takes a city, state, zip, and country to return latitude and longitude, and another that takes a locode and returns the corresponding latitude and longitude.

## Setup
   1. Use venv to create a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   2. Install Requirements:
   ```bash
   pip install -r requirements.txt
   ```
   3. Run the server:
   ```bash
   python app.py
   ```

## Usage
Using the server is simple. To start the server, run the following command:
```bash
python app.py
```

To run the tests, run the following command:
```bash
python test_server.py
```

To send a POST request to the server, you can use the following curl command:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"city": "New York", "state": "NY", "zip": "10001", "country": "US"}' http://localhost:5001/geocode

curl -X POST -H "Content-Type: application/json" -d '{"locode": "US NYC"}' http://localhost:5001/geocode
```

## Request Body Structure
The server accepts POST requests at the `/geocode` endpoint. The request body should be a JSON object with the following structure:
1. For city, state, zip, and country:
```json
{
    "city": "city",
    "state": "state",
    "zip": "zip",
    "country": "country"
}
```
2. For locode (The locode should be in the format "COUNTRY LOCATION" with a space in between):
```json
{
    "locode": "LOCODE"
}
```
3. Just zip and country (Technically not part of the requirements, but I allowed it because the API supports it):
```json
{
    "zip": "zip",
    "country": "country"
}
```
