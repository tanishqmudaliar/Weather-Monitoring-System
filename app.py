import os
import subprocess
import hmac
import hashlib
import requests
import threading
import time
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Environment variables
API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
PYTHONANYWHERE_API_TOKEN = os.getenv("PYTHONANYWHERE_API_TOKEN")
PYTHONANYWHERE_USERNAME = os.getenv("PYTHONANYWHERE_USERNAME")
PROJECT_PATH = f"/home/{PYTHONANYWHERE_USERNAME}/Weather-Monitoring-System" if PYTHONANYWHERE_USERNAME else "."
DEPLOYMENT_LOG = f"{PROJECT_PATH}/deployment.log"
BASE_URL = "https://api.openweathermap.org/data/2.5"


def log_deployment(message):
    """Write deployment events to log file"""
    try:
        with open(DEPLOYMENT_LOG, 'a') as f:
            timestamp = datetime.now().isoformat()
            f.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        print(f"Failed to write log: {e}")


def push_log_to_github():
    """Commit and push deployment log to GitHub"""
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_message = f"Server reload successful - {timestamp}"

        subprocess.run(['git', 'add', 'deployment.log'], cwd=PROJECT_PATH, capture_output=True, timeout=10)

        commit_result = subprocess.run(
            ['git', 'commit', '-m', commit_message],
            cwd=PROJECT_PATH, capture_output=True, text=True, timeout=10
        )

        if commit_result.returncode == 0:
            push_result = subprocess.run(
                ['git', 'push', 'origin', 'master'],
                cwd=PROJECT_PATH, capture_output=True, text=True, timeout=30
            )
            if push_result.returncode == 0:
                log_deployment(f"✓ Log pushed to GitHub: {commit_message}")
            else:
                log_deployment(f"✗ Git push failed: {push_result.stderr.strip()}")
        else:
            log_deployment("No new log entries to push")
    except Exception as e:
        log_deployment(f"✗ Git push error: {str(e)}")


def reload_webapp_async(delay=3):
    """Reload webapp after delay in background thread"""

    def do_reload():
        time.sleep(delay)
        log_deployment("Starting webapp reload...")

        if PYTHONANYWHERE_API_TOKEN and PYTHONANYWHERE_USERNAME:
            try:
                reload_response = requests.post(
                    f'https://www.pythonanywhere.com/api/v0/user/{PYTHONANYWHERE_USERNAME}/webapps/{PYTHONANYWHERE_USERNAME}.pythonanywhere.com/reload/',
                    headers={'Authorization': f'Token {PYTHONANYWHERE_API_TOKEN}'},
                    timeout=30
                )
                if reload_response.ok:
                    log_deployment("✓ Reload API call successful")
                else:
                    log_deployment(f"✗ Reload API failed: {reload_response.status_code}")
            except Exception as e:
                log_deployment(f"✗ Reload error: {str(e)}")
        else:
            log_deployment("✗ No API token - cannot reload")

    thread = threading.Thread(target=do_reload, daemon=True)
    thread.start()


# Log server startup
log_deployment("=" * 60)
log_deployment("SERVER STARTED SUCCESSFULLY")
log_deployment(f"Flask app initialized at {datetime.now().isoformat()}")
log_deployment("=" * 60)
threading.Thread(target=push_log_to_github, daemon=True).start()


@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    """Handle GitHub webhook for auto-deployment"""
    if WEBHOOK_SECRET:
        signature = request.headers.get('X-Hub-Signature-256', '')
        expected_sig = 'sha256=' + hmac.new(
            WEBHOOK_SECRET.encode(), request.data, hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(signature, expected_sig):
            log_deployment("✗ Webhook rejected: invalid signature")
            return jsonify({'error': 'Invalid signature'}), 403

    event = request.headers.get('X-GitHub-Event', '')

    if event == 'ping':
        log_deployment("Webhook ping received")
        return jsonify({'status': 'pong'}), 200

    if event != 'push':
        return jsonify({'status': 'ignored', 'reason': f'Event: {event}'}), 200

    payload = request.get_json()
    ref = payload.get('ref', '')
    commit_msg = payload.get('head_commit', {}).get('message', '')
    commit_id = payload.get('head_commit', {}).get('id', 'unknown')[:7]

    if commit_msg.startswith("Server reload successful"):
        log_deployment(f"Ignoring self-generated commit: {commit_id}")
        return jsonify({'status': 'ignored', 'reason': 'Log push commit'}), 200

    if ref not in ['refs/heads/master', 'refs/heads/main']:
        return jsonify({'status': 'ignored', 'reason': f'Push to {ref}'}), 200

    log_deployment(f"Webhook received: {ref} - {commit_id} - {commit_msg}")

    try:
        pull_result = subprocess.run(
            ['git', 'pull', 'origin', 'master'],
            cwd=PROJECT_PATH, capture_output=True, text=True, timeout=60
        )
        if pull_result.returncode == 0:
            log_deployment(f"✓ Git pull successful")
        else:
            log_deployment(f"✗ Git pull failed: {pull_result.stderr}")
    except Exception as e:
        log_deployment(f"✗ Git pull error: {str(e)}")
        return jsonify({'error': str(e)}), 500

    try:
        subprocess.run(
            ['pip', 'install', '-r', 'requirements.txt', '--user', '--quiet'],
            cwd=PROJECT_PATH, capture_output=True, timeout=120
        )
        log_deployment("✓ Dependencies installed")
    except Exception as e:
        log_deployment(f"! Pip install warning: {str(e)}")

    reload_webapp_async(delay=3)
    log_deployment("Webhook response sent, reload scheduled")

    return jsonify({
        'status': 'deployment_started',
        'branch': ref,
        'commit': commit_id,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/deployment-log')
def view_deployment_log():
    """View deployment log for debugging"""
    try:
        with open(DEPLOYMENT_LOG, 'r') as f:
            logs = f.read()
        return f"<pre>{logs}</pre>", 200
    except FileNotFoundError:
        return "No deployment log found", 404
    except Exception as e:
        return f"Error: {e}", 500


@app.route('/')
def home():
    """Render main page"""
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return send_from_directory(app.static_folder, 'favicon.ico')


@app.route('/api/reverse-geocode')
def reverse_geocode():
    """Get city name from coordinates"""
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    if not (lat and lon):
        return jsonify({"error": "Missing coordinates"}), 400
    if not API_KEY:
        return jsonify({"error": "Server misconfigured"}), 500

    url = f"https://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={API_KEY}"

    try:
        r = requests.get(url, timeout=5)
        if not r.ok:
            return jsonify({"error": "Geocoding failed"}), r.status_code

        arr = r.json()
        if not arr:
            return jsonify({"error": "No results"}), 404

        city = arr[0].get("name")
        return jsonify({"city": city, "raw": arr[0]})
    except requests.RequestException:
        return jsonify({"error": "Service unavailable"}), 502


@app.route('/api/current-weather')
def get_current_weather():
    """Fetch current weather data"""
    location = request.args.get('location', '')
    if not location:
        return jsonify({"error": "Location required"}), 400

    url = f"{BASE_URL}/weather?q={location}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return jsonify({"error": "Weather data unavailable"}), response.status_code

        data = response.json()

        # Fetch UV index from Open-Meteo (free API)
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        uv_index = get_uv_index_from_open_meteo(lat, lon)

        weather_data = {
            "location": f"{data['name']}, {data.get('sys', {}).get('country', '')}",
            "temperature": data['main']['temp'],
            "feels_like": data['main']['feels_like'],
            "temp_min": data['main']['temp_min'],
            "temp_max": data['main']['temp_max'],
            "description": data['weather'][0]['description'].title(),
            "icon": data['weather'][0]['icon'],
            "humidity": data['main']['humidity'],
            "pressure": data['main']['pressure'],
            "wind_speed": data['wind']['speed'],
            "wind_direction": data['wind'].get('deg', 0),
            "wind_gust": data['wind'].get('gust', data['wind']['speed']),
            "clouds": data.get('clouds', {}).get('all', 0),
            "visibility": data.get('visibility', 10000),
            "timestamp": data['dt'],
            "sunrise": data['sys']['sunrise'],
            "sunset": data['sys']['sunset'],
            "timezone": data.get('timezone', 0),
            "uv_index": uv_index,
            "rain_1h": data.get('rain', {}).get('1h', 0),
            "snow_1h": data.get('snow', {}).get('1h', 0)
        }

        return jsonify(weather_data)
    except requests.RequestException:
        return jsonify({"error": "Service unavailable"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/forecast')
def get_forecast():
    """Fetch 5-day forecast"""
    location = request.args.get('location', '')
    if not location:
        return jsonify({"error": "Location required"}), 400

    # Get coordinates
    geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}"

    try:
        geo_response = requests.get(geo_url, timeout=10)
        if geo_response.status_code != 200 or not geo_response.json():
            return jsonify({"error": "Location not found"}), 400

        coords = geo_response.json()[0]
        lat, lon = coords['lat'], coords['lon']

        # Get forecast
        forecast_url = f"{BASE_URL}/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(forecast_url, timeout=10)

        if response.status_code != 200:
            return jsonify({"error": "Forecast unavailable"}), response.status_code

        data = response.json()

        processed_forecast = []
        for item in data['list']:
            processed_forecast.append({
                "dt": item['dt'],
                "date": datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S'),
                "temp": item['main']['temp'],
                "feels_like": item['main']['feels_like'],
                "temp_min": item['main']['temp_min'],
                "temp_max": item['main']['temp_max'],
                "description": item['weather'][0]['description'].title(),
                "icon": item['weather'][0]['icon'],
                "humidity": item['main']['humidity'],
                "pressure": item['main']['pressure'],
                "wind_speed": item['wind']['speed'],
                "wind_direction": item['wind'].get('deg', 0),
                "clouds": item['clouds']['all'],
                "pop": item.get('pop', 0) * 100,  # Probability of precipitation
                "rain_3h": item.get('rain', {}).get('3h', 0),
                "snow_3h": item.get('snow', {}).get('3h', 0)
            })

        return jsonify(processed_forecast)
    except requests.RequestException:
        return jsonify({"error": "Service unavailable"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/air-quality')
def get_air_quality():
    """Fetch air quality data"""
    location = request.args.get('location', '')
    if not location:
        return jsonify({"error": "Location required"}), 400

    # Get coordinates
    geo_url = f"https://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}"

    try:
        geo_response = requests.get(geo_url, timeout=10)
        if geo_response.status_code != 200 or not geo_response.json():
            return jsonify({"error": "Location not found"}), 400

        coords = geo_response.json()[0]
        lat, lon = coords['lat'], coords['lon']

        # Get air quality
        aqi_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        response = requests.get(aqi_url, timeout=10)

        if response.status_code != 200:
            return jsonify({"error": "Air quality data unavailable"}), response.status_code

        data = response.json()

        if 'list' in data and len(data['list']) > 0:
            aqi_data = data['list'][0]
            components = aqi_data.get('components', {})

            # OpenWeather AQI is 1-5 scale (European CAQI)
            # Convert to US EPA scale (0-500) for better representation
            pm25 = components.get('pm2_5', 0)

            # Calculate US EPA AQI from PM2.5 (more accurate)
            us_aqi = calculate_us_aqi_from_pm25(pm25) if pm25 > 0 else aqi_data['main']['aqi'] * 50

            return jsonify({
                "aqi": round(us_aqi),
                "pm25": components.get('pm2_5', 0),
                "pm10": components.get('pm10', 0),
                "o3": components.get('o3', 0),
                "no2": components.get('no2', 0),
                "so2": components.get('so2', 0),
                "co": components.get('co', 0)
            })
        else:
            return jsonify({"error": "No air quality data"}), 404

    except requests.RequestException:
        return jsonify({"error": "Service unavailable"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def calculate_us_aqi_from_pm25(pm25):
    """Convert PM2.5 to US EPA AQI scale"""
    # US EPA AQI breakpoints for PM2.5
    breakpoints = [
        (0, 12.0, 0, 50),  # Good
        (12.1, 35.4, 51, 100),  # Moderate
        (35.5, 55.4, 101, 150),  # Unhealthy for Sensitive Groups
        (55.5, 150.4, 151, 200),  # Unhealthy
        (150.5, 250.4, 201, 300),  # Very Unhealthy
        (250.5, 500.4, 301, 500)  # Hazardous
    ]

    for low_c, high_c, low_i, high_i in breakpoints:
        if low_c <= pm25 <= high_c:
            aqi = ((high_i - low_i) / (high_c - low_c)) * (pm25 - low_c) + low_i
            return round(aqi)

    # If PM2.5 is above all breakpoints
    return 500


def get_uv_index_from_open_meteo(lat, lon):
    """Fetch UV index from Open-Meteo API (completely free, no API key needed)"""
    try:
        # Open-Meteo is a free weather API with UV index support
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=uv_index&timezone=auto"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            uv_value = data.get('current', {}).get('uv_index', 0)
            return round(uv_value, 1)
        else:
            return 0
    except Exception as e:
        print(f"UV Index fetch error: {e}")
        return 0


if __name__ == '__main__':
    app.run(debug=True)