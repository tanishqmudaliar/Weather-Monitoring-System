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

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Get API key from environment variables
API_KEY = os.getenv("OPENWEATHER_API_KEY")
WEBHOOK_SECRET = os.getenv("GITHUB_WEBHOOK_SECRET")
PYTHONANYWHERE_API_TOKEN = os.getenv("PYTHONANYWHERE_API_TOKEN")
PYTHONANYWHERE_USERNAME = os.getenv("PYTHONANYWHERE_USERNAME")
PROJECT_PATH = f"/home/{PYTHONANYWHERE_USERNAME}/Weather-Monitoring-System"
DEPLOYMENT_LOG = f"{PROJECT_PATH}/deployment.log"
BASE_URL = "https://api.openweathermap.org/data/2.5"

def log_deployment(message):
    """Write deployment events to a persistent log file"""
    try:
        with open(DEPLOYMENT_LOG, 'a') as f:
            timestamp = datetime.now().isoformat()
            f.write(f"[{timestamp}] {message}\n")
    except Exception as e:
        print(f"Failed to write log: {e}")

def push_log_to_github():
    """
    Commit and push deployment.log to GitHub with timestamped message.
    Runs after server successfully reloads.
    """
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        commit_message = f"Server reload successful - {timestamp}"

        # Add deployment.log to git
        subprocess.run(
            ['git', 'add', 'deployment.log'],
            cwd=PROJECT_PATH,
            capture_output=True,
            timeout=10
        )

        # Commit with timestamped message
        commit_result = subprocess.run(
            ['git', 'commit', '-m', commit_message],
            cwd=PROJECT_PATH,
            capture_output=True,
            text=True,
            timeout=10
        )

        # Only push if there was something to commit
        if commit_result.returncode == 0:
            push_result = subprocess.run(
                ['git', 'push', 'origin', 'master'],
                cwd=PROJECT_PATH,
                capture_output=True,
                text=True,
                timeout=30
            )

            if push_result.returncode == 0:
                log_deployment(f"✓ Log pushed to GitHub: {commit_message}")
            else:
                log_deployment(f"✗ Git push failed: {push_result.stderr.strip()}")
        else:
            # No changes to commit (this is fine)
            log_deployment("No new log entries to push")

    except subprocess.TimeoutExpired:
        log_deployment("✗ Git push timed out")
    except Exception as e:
        log_deployment(f"✗ Git push error: {str(e)}")

def reload_webapp_async(delay=3):
    """
    Reload the webapp after a delay, running in background thread.
    This allows the webhook response to be sent before reload.
    """
    def do_reload():
        time.sleep(delay)  # Wait for response to be sent

        log_deployment("Starting webapp reload...")

        if PYTHONANYWHERE_API_TOKEN:
            try:
                reload_response = requests.post(
                    f'https://www.pythonanywhere.com/api/v0/user/{PYTHONANYWHERE_USERNAME}/webapps/{PYTHONANYWHERE_USERNAME}.pythonanywhere.com/reload/',
                    headers={'Authorization': f'Token {PYTHONANYWHERE_API_TOKEN}'},
                    timeout=30
                )

                if reload_response.ok:
                    log_deployment("✓ Reload API call successful - webapp should restart shortly")
                else:
                    log_deployment(f"✗ Reload API failed: HTTP {reload_response.status_code} - {reload_response.text}")

            except Exception as e:
                log_deployment(f"✗ Reload error: {str(e)}")
        else:
            log_deployment("✗ No PYTHONANYWHERE_API_TOKEN - cannot reload")

    # Start reload in background thread
    thread = threading.Thread(target=do_reload, daemon=True)
    thread.start()

# Log server startup and push to GitHub
log_deployment("=" * 60)
log_deployment("SERVER STARTED SUCCESSFULLY")
log_deployment(f"Flask app initialized at {datetime.now().isoformat()}")
log_deployment("=" * 60)

# Push the log to GitHub after successful startup (in background to not delay startup)
threading.Thread(target=push_log_to_github, daemon=True).start()

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    """
    Receives GitHub webhook, pulls latest code, schedules reload.
    Returns response BEFORE reload to avoid webhook timeout.
    """

    # Step 1: Verify webhook signature (security)
    if WEBHOOK_SECRET:
        signature = request.headers.get('X-Hub-Signature-256', '')
        expected_sig = 'sha256=' + hmac.new(
            WEBHOOK_SECRET.encode(),
            request.data,
            hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(signature, expected_sig):
            log_deployment("✗ Webhook rejected: invalid signature")
            return jsonify({'error': 'Invalid signature'}), 403

    # Step 2: Check if it's a push event
    event = request.headers.get('X-GitHub-Event', '')

    if event == 'ping':
        log_deployment("Webhook ping received")
        return jsonify({'status': 'pong', 'message': 'Webhook configured successfully!'}), 200

    if event != 'push':
        return jsonify({'status': 'ignored', 'reason': f'Event type: {event}'}), 200

    # Step 3: Parse payload and check branch
    payload = request.get_json()
    ref = payload.get('ref', '')
    commit_msg = payload.get('head_commit', {}).get('message', 'No message')
    commit_id = payload.get('head_commit', {}).get('id', 'unknown')[:7]

    # Ignore commits that are from the log push itself (prevent infinite loop)
    if commit_msg.startswith("Server reload successful"):
        log_deployment(f"Ignoring self-generated commit: {commit_id}")
        return jsonify({'status': 'ignored', 'reason': 'Log push commit'}), 200

    if ref not in ['refs/heads/master', 'refs/heads/main']:
        return jsonify({
            'status': 'ignored',
            'reason': f'Push to {ref}, not master/main'
        }), 200

    log_deployment(f"Webhook received: {ref} - {commit_id} - {commit_msg}")

    # Step 4: Pull latest code from GitHub
    try:
        pull_result = subprocess.run(
            ['git', 'pull', 'origin', 'master'],
            cwd=PROJECT_PATH,
            capture_output=True,
            text=True,
            timeout=60
        )

        git_output = pull_result.stdout + pull_result.stderr

        if pull_result.returncode == 0:
            log_deployment(f"✓ Git pull successful: {git_output.strip()}")
        else:
            log_deployment(f"✗ Git pull failed: {git_output.strip()}")

    except subprocess.TimeoutExpired:
        log_deployment("✗ Git pull timed out")
        return jsonify({'error': 'Git pull timed out'}), 500
    except Exception as e:
        log_deployment(f"✗ Git pull error: {str(e)}")
        return jsonify({'error': f'Git pull failed: {str(e)}'}), 500

    # Step 5: Install any new dependencies
    try:
        pip_result = subprocess.run(
            ['pip', 'install', '-r', 'requirements.txt', '--user', '--quiet'],
            cwd=PROJECT_PATH,
            capture_output=True,
            text=True,
            timeout=120
        )
        if pip_result.returncode == 0:
            log_deployment("✓ Dependencies installed")
        else:
            log_deployment(f"! Pip install warning: {pip_result.stderr}")
    except Exception as e:
        log_deployment(f"! Pip install error (non-fatal): {str(e)}")

    # Step 6: Schedule reload in background (after response is sent)
    reload_webapp_async(delay=3)

    log_deployment("Webhook response sent, reload scheduled in 3 seconds...")

    # Step 7: Return success response IMMEDIATELY (before reload)
    return jsonify({
        'status': 'deployment_started',
        'message': 'Code pulled, reload scheduled',
        'branch': ref,
        'commit': commit_id,
        'reload_scheduled': True,
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/deployment-log')
def view_deployment_log():
    """View deployment log (for debugging)"""
    try:
        with open(DEPLOYMENT_LOG, 'r') as f:
            logs = f.read()
        return f"<pre>{logs}</pre>", 200
    except FileNotFoundError:
        return "No deployment log found", 404
    except Exception as e:
        return f"Error reading log: {e}", 500

@app.route('/')
def home():
    """Render the main page"""
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    """Serve the favicon"""
    return send_from_directory(app.static_folder, 'favicon.ico')


@app.route('/get_weather', methods=['GET'])
def get_weather():
    """Fetch current weather data for a given city"""
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
        response = requests.get(f"{BASE_URL}/weather", params=params)
        data = response.json()

        if response.status_code == 200:
            return jsonify(data)
        else:
            return jsonify({'error': data.get('message', 'Error fetching weather data')}), response.status_code

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route("/api/reverse-geocode")
def reverse_geocode():
    """Get city name from latitude and longitude using OpenWeatherMap Geocoding API"""
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
    """Fetch current weather data for a given location"""
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
        "visibility": data.get('visibility', 10000),
        "timestamp": data['dt'],
        "sunrise": data['sys']['sunrise'],
        "sunset": data['sys']['sunset']
    }

    return jsonify(weather_data)


@app.route('/api/forecast')
def get_forecast():
    """Fetch 5-day weather forecast for a given location"""
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