import os
import requests
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get API key from environment variables
API_KEY = os.getenv("OPENWEATHER_API_KEY")
if not API_KEY:
    raise ValueError("No OpenWeather API key found. Please set OPENWEATHER_API_KEY in .env file")

BASE_URL = "https://api.openweathermap.org/data/2.5"


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.static_folder, 'favicon.ico')

@app.route('/get_weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')

    if not city:
        return jsonify({'error': 'City name is required'}), 400

    # Parameters for OpenWeatherMap API
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }

    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if response.status_code == 200:
            return jsonify(data)
        else:
            return jsonify({'error': data.get('message', 'Error fetching weather data')}), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/reverse-geocode")
def reverse_geocode():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if not (lat and lon):
        return jsonify({"error": "missing coordinates"}), 400
    if not API_KEY:
        return jsonify({"error": "server misconfigured"}), 500

    url = f"https://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={API_KEY}"
    try:
        r = requests.get(url, timeout=5)
    except requests.RequestException:
        return jsonify({"error": "failed to contact geocoding service"}), 502

    if not r.ok:
        return jsonify({"error": "geocoding failed"}), r.status_code

    arr = r.json()
    if not arr:
        return jsonify({"error": "no results"}), 404

    city = arr[0].get("name")
    return jsonify({"city": city, "raw": arr[0]})


@app.route('/api/current-weather')
def get_current_weather():
    location = request.args.get('location', '')
    if not location:
        return jsonify({"error": "Location parameter is required"}), 400

    url = f"{BASE_URL}/weather?q={location}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "Could not retrieve weather data"}), response.status_code

    data = response.json()
    weather_data = {
        "location": f"{data['name']}, {data.get('sys', {}).get('country', '')}",
        "temperature": data['main']['temp'],
        "feels_like": data['main']['feels_like'],
        "description": data['weather'][0]['description'],
        "icon": data['weather'][0]['icon'],
        "humidity": data['main']['humidity'],
        "pressure": data['main']['pressure'],
        "wind_speed": data['wind']['speed'],
        "wind_direction": data['wind']['deg'],
        "clouds": data.get('clouds', {}).get('all', 0),
        "visibility": data.get('visibility', 10000),  # Added visibility
        "timestamp": data['dt'],
        "sunrise": data['sys']['sunrise'],
        "sunset": data['sys']['sunset']
    }

    return jsonify(weather_data)


@app.route('/api/forecast')
def get_forecast():
    location = request.args.get('location', '')

    if not location:
        return jsonify({"error": "Location parameter is required"}), 400

    # Get coordinates for the location
    geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}"
    geo_response = requests.get(geo_url)

    if geo_response.status_code != 200 or not geo_response.json():
        return jsonify({"error": "Could not find coordinates for location"}), 400

    coords = geo_response.json()[0]
    lat, lon = coords['lat'], coords['lon']

    # Get 5-day forecast
    forecast_url = f"{BASE_URL}/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    response = requests.get(forecast_url)

    if response.status_code != 200:
        return jsonify({"error": "Could not retrieve forecast data"}), response.status_code

    data = response.json()

    # Process forecast data
    processed_forecast = []
    for item in data['list']:
        processed_forecast.append({
            "dt": item['dt'],
            "date": datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S'),
            "temp": item['main']['temp'],
            "feels_like": item['main']['feels_like'],
            "temp_min": item['main']['temp_min'],
            "temp_max": item['main']['temp_max'],
            "description": item['weather'][0]['description'],
            "icon": item['weather'][0]['icon'],
            "humidity": item['main']['humidity'],
            "pressure": item['main']['pressure'],
            "wind_speed": item['wind']['speed'],
            "wind_direction": item['wind']['deg'],
            "clouds": item['clouds']['all']
        })

    return jsonify(processed_forecast)


if __name__ == '__main__':
    app.run(debug=True)