import os
import sys
import logging
import subprocess
import hmac
import hashlib
import requests
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

app.logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

# Log at startup to verify logging works
app.logger.info("App starting - PA_TOKEN exists: %s, PA_USER: %s",
                bool(os.getenv('PYTHONANYWHERE_API_TOKEN')),
                os.getenv('PYTHONANYWHERE_USERNAME'))

# Get API key from environment variables
API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
PYTHONANYWHERE_API_TOKEN = os.getenv("PYTHONANYWHERE_API_TOKEN")
PYTHONANYWHERE_USERNAME = os.getenv("PYTHONANYWHERE_USERNAME")
BASE_URL = "https://api.openweathermap.org/data/2.5"
PROJECT_PATH = f"/home/{PYTHONANYWHERE_USERNAME}/Weather-Monitoring-System"

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    """
    Receives GitHub webhook, pulls latest code, and reloads the webapp.
    Fully automated deployment on every push to master.
    """
    app.logger.info("ENV CHECK - PA_TOKEN exists: %s, length: %s",
                    bool(PYTHONANYWHERE_API_TOKEN),
                    len(PYTHONANYWHERE_API_TOKEN) if PYTHONANYWHERE_API_TOKEN else 0)
    app.logger.info("ENV CHECK - PA_USER: %s", PYTHONANYWHERE_USERNAME)
    # Verify signature (unchanged)
    if WEBHOOK_SECRET:
        signature = request.headers.get('X-Hub-Signature-256', '')
        expected_sig = 'sha256=' + hmac.new(
            WEBHOOK_SECRET.encode(),
            request.data,
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(signature, expected_sig):
            return jsonify({'error': 'Invalid signature'}), 403

    event = request.headers.get('X-GitHub-Event', '')
    if event == 'ping':
        return jsonify({'status': 'pong', 'message': 'Webhook configured successfully! '}), 200
    if event != 'push':
        return jsonify({'status': 'ignored', 'reason': f'Event type:  {event}'}), 200

    payload = request.get_json()
    ref = payload.get('ref', '')
    if ref not in ['refs/heads/master', 'refs/heads/main']:
        return jsonify({'status': 'ignored', 'reason': f'Push to {ref}, not master/main'}), 200

    # Determine branch name from ref
    branch = ref.split('/')[-1]

    # Step 4: Pull latest code
    try:
        pull_result = subprocess.run(
            ['git', 'pull', 'origin', branch],
            cwd=PROJECT_PATH,
            capture_output=True,
            text=True,
            timeout=60
        )
        git_output = (pull_result.stdout or '') + (pull_result.stderr or '')
    except subprocess.TimeoutExpired:
        return jsonify({'error': 'Git pull timed out'}), 500
    except Exception as e:
        return jsonify({'error': f'Git pull failed: {str(e)}'}), 500

    # Step 5: Install dependencies (capture output; non-fatal)
    try:
        pip_proc = subprocess.run(
            ['pip', 'install', '-r', 'requirements.txt', '--user', '--quiet'],
            cwd=PROJECT_PATH,
            capture_output=True,
            text=True,
            timeout=120
        )
        pip_output = (pip_proc.stdout or '') + (pip_proc.stderr or '')
    except Exception as e:
        pip_output = f'pip install failed or timed out: {str(e)}'

    # Step 6: Reload the webapp via PythonAnywhere API (improved logging)
    reload_status = "skipped"
    if PYTHONANYWHERE_API_TOKEN and PYTHONANYWHERE_USERNAME:
        try:
            url = f'https://www.pythonanywhere.com/api/v0/user/{PYTHONANYWHERE_USERNAME}/webapps/{PYTHONANYWHERE_USERNAME}.pythonanywhere.com/reload/'
            reload_response = requests.post(
                url,
                headers={'Authorization': f'Token {PYTHONANYWHERE_API_TOKEN}'},
                timeout=30
            )
            resp_text = (reload_response.text or "").strip()
            # Try to include JSON body if available for clearer logs
            try:
                resp_body = reload_response.json()
            except Exception:
                resp_body = resp_text

            if reload_response.ok:
                reload_status = "success"
            else:
                reload_status = f"failed: {reload_response.status_code} - {str(resp_body)[:1000]}"
                app.logger.error("PythonAnywhere reload failed (%s): %s", reload_response.status_code, resp_text)
        except requests.RequestException as e:
            reload_status = f"error: {str(e)}"
            app.logger.exception("Exception when calling PythonAnywhere API")

    # Step 7: Return response
    return jsonify({
        'status': 'deployed',
        'branch': ref,
        'git_output': git_output,
        'reload_status': reload_status,
        'timestamp': datetime.now().isoformat(),
        'pip_output': pip_output
    }), 200

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