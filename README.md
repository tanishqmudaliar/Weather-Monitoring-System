# Weather Monitoring System

A modern, responsive web application for monitoring real-time weather conditions and forecasts powered by the OpenWeatherMap API.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Deploy](https://img.shields.io/badge/Deploy-Automated-brightgreen.svg)
![PythonAnywhere](https://img.shields.io/badge/Hosted-PythonAnywhere-orange.svg)

**[Live Demo](https://tanishqmudaliar.pythonanywhere.com)** | **[Auto-Renew Bot](https://github.com/tanishqmudaliar/PythonAnywhere-Auto-Renew)**

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Docker Setup (Recommended)](#-docker-setup-recommended---zero-configuration)
  - [Local Development (Without Docker)](#-local-development-without-docker)
  - [PythonAnywhere Deployment](#pythonanywhere-deployment)
- [API Reference](#api-reference)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [Related Repositories](#related-repositories)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

---

## Overview

Weather Monitoring System is a full-stack weather application that provides real-time weather data and 5-day forecasts for any city worldwide. Built with Flask and vanilla JavaScript, it features a modern UI with interactive charts, unit conversion, and geolocation support.

The project implements a fully automated CI/CD pipeline—every push to `master` triggers an automatic deployment to PythonAnywhere. Combined with the [PythonAnywhere-Auto-Renew](https://github.com/tanishqmudaliar/PythonAnywhere-Auto-Renew) bot, this creates a zero-maintenance hosting solution that stays alive indefinitely on the free tier.

---

## Features

### Current Weather

- Real-time weather data for any city worldwide
- Temperature, feels-like, humidity, pressure, and wind metrics
- Pressure readings: atmospheric, sea level, and ground level (hPa)
- UV index via Open-Meteo API integration
- Sunrise/sunset times with timezone support
- **Weather Alerts**: Automatic warnings for severe conditions (thunderstorms, heavy rain, snow, fog, tornadoes)
- Air quality index (AQI) with full pollutant breakdown (PM2.5, PM10, O₃, NO₂, NO, SO₂, CO, NH₃)

### 5-Day Forecast

- Extended weather predictions with 3-hour intervals
- Interactive temperature trend charts (Chart.js)
- Daily summaries with average temperature and humidity
- Precipitation probability and rain/snow forecasts

### User Experience

- **Unit Toggle**: Switch between Metric (°C) and Imperial (°F)
- **Geolocation**: Auto-detect user's current location
- **Responsive Design**: Optimized for desktop, tablet, and mobile
- **Modern UI**: Clean interface with Font Awesome icons

### DevOps

- Zero-downtime automated deployment via GitHub Actions
- Deployment logging viewable at `/deployment-log`
- Auto-renewal integration for free-tier hosting
- Docker containerization for easy local development

---

## Tech Stack

| Layer                | Technologies                             |
| -------------------- | ---------------------------------------- |
| **Backend**          | Python 3.14, Flask 3.0.0                 |
| **Frontend**         | HTML5, CSS3, JavaScript (ES6+), Chart.js |
| **APIs**             | OpenWeatherMap, Open-Meteo (UV Index)    |
| **Containerization** | Docker, Docker Compose                   |
| **Deployment**       | PythonAnywhere                           |
| **CI/CD**            | GitHub Actions                           |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FULLY AUTOMATED PYTHONANYWHERE HOSTING                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                              GITHUB                                  │   │
│  │                                                                      │   │
│  │   ┌─────────────────────────────┐  ┌─────────────────────────────┐   │   │
│  │   │  Weather-Monitoring-System  │  │  PythonAnywhere-Auto-Renew  │   │   │
│  │   │                             │  │                             │   │   │
│  │   │  • Main application code    │  │  • Renewal bot              │   │   │
│  │   │  • Deployment endpoint      │  │  • Runs 1st & 15th monthly  │   │   │
│  │   │  • Auto-deploys on push     │  │  • Keeps app alive forever  │   │   │
│  │   └──────────────┬──────────────┘  └──────────────┬──────────────┘   │   │
│  │                  │ POST request                   │ Github           │   │
│  │                  │ (/github-webhook)              │ Actions          │   │
│  │                  ▼                                ▼                  │   │
│  └──────────────────┼────────────────────────────────┼──────────────────┘   │
│                     │                                │                      │
│  ┌──────────────────▼────────────────────────────────▼──────────────────┐   │
│  │                            PYTHONANYWHERE                            │   │
│  │                                                                      │   │
│  │      ┌─────────────────────────┐    ┌─────────────────────────┐      │   │
│  │      │   Deployment Endpoint   │    │     Auto-Renewal        │      │   │
│  │      │  • git pull             │    │  • Extends app expiry   │      │   │
│  │      │  • pip install          │    │  • Prevents shutdown    │      │   │
│  │      │  • Reload webapp        │    │  • Zero maintenance     │      │   │
│  │      └─────────────────────────┘    └─────────────────────────┘      │   │
│  │                                                                      │   │
│  │              https://tanishqmudaliar.pythonanywhere.com              │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│               Push code → Instantly live → Stays alive forever              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Deployment Flow

1. Push code to `master` or `main` branch
2. GitHub Actions workflow sends POST request to `/github-webhook` endpoint
3. Flask endpoint pulls latest code via `git pull`
4. Dependencies are installed with `pip install -r requirements.txt`
5. PythonAnywhere API reloads the webapp
6. Changes are live within seconds

---

## Getting Started

### Prerequisites

- **For Docker (Recommended)**: [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed
- **For Local Development**: Python 3.8+ and OpenWeatherMap API key ([Get one free](https://home.openweathermap.org/api_keys))

---

## 🐳 Docker Setup (Recommended - Zero Configuration)

The easiest way to run the Weather Monitoring System locally is with Docker. No Python installation or dependency management required!

### Quick Start

1. **Clone the repository**

```bash
   git clone https://github.com/tanishqmudaliar/Weather-Monitoring-System.git
   cd Weather-Monitoring-System
```

2. **Create environment file**

```bash
   cp .env.example .env
```

3. **Add your OpenWeather API key**

   Edit `.env` and replace the placeholder:

```env
   OPENWEATHER_API_KEY=your_actual_api_key_here
```

Get your free API key from [OpenWeatherMap](https://home.openweathermap.org/api_keys)

4. **Start the application**

```bash
   docker compose up -d
```

5. **Access the application**

   Open your browser: **http://localhost:5000**

### Docker Commands Reference

| Command                        | Description                                         |
| ------------------------------ | --------------------------------------------------- |
| `docker compose up -d`         | Start the application in background (detached mode) |
| `docker compose down`          | Stop and remove the application container           |
| `docker compose logs -f`       | View real-time application logs                     |
| `docker compose restart`       | Restart the application                             |
| `docker compose ps`            | Check container status                              |
| `docker compose down -v`       | Stop and remove container + delete all data/logs    |
| `docker compose up --build -d` | Rebuild and start (after code changes)              |

### Docker Troubleshooting

**Port 5000 already in use?**

Edit `docker-compose.yml` and change the port mapping:

```yaml
ports:
  - "8080:5000" # Now access at http://localhost:8080
```

**Container won't start?**

```bash
# Check logs for errors
docker compose logs weather-app

# Rebuild the container
docker compose down
docker compose up --build -d
```

**Can't connect to http://localhost:5000?**

- Ensure Docker Desktop is running
- Check container health: `docker compose ps`
- Verify the container shows as "Up" and "healthy"
- Check your `.env` file has a valid API key

**Need to update code?**

```bash
# After making code changes
docker compose restart  # Quick restart
# OR
docker compose up --build -d  # Full rebuild
```

---

## 💻 Local Development (Without Docker)

If you prefer to run without Docker or need to develop/debug the application:

### Prerequisites

- Python 3.8+ (developed with 3.14)
- OpenWeatherMap API key ([Get one free](https://home.openweathermap.org/api_keys))

### Setup Steps

1. **Clone the repository**

```bash
   git clone https://github.com/tanishqmudaliar/Weather-Monitoring-System.git
   cd Weather-Monitoring-System
```

2. **Create and activate a virtual environment** (recommended)

```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
```

3. **Install dependencies**

```bash
   pip install -r requirements.txt
```

4. **Configure environment variables**

   Create a `.env` file in the project root:

```env
   OPENWEATHER_API_KEY=your_api_key_here
```

5. **Run the application**

```bash
   python app.py
```

6. **Open your browser**

   Navigate to `http://127.0.0.1:5000`

---

## PythonAnywhere Deployment

#### Step 1: Initial Setup

1. Create a free account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Open a Bash console and clone the repository:

```bash
   git clone https://github.com/tanishqmudaliar/Weather-Monitoring-System.git
```

3. Set up your web app pointing to the cloned directory

4. Create a `.env` file with your credentials:

```env
   OPENWEATHER_API_KEY=your_openweather_key
   GITHUB_WEBHOOK_SECRET=your_random_secret
   PYTHONANYWHERE_API_TOKEN=your_api_token
   PYTHONANYWHERE_USERNAME=your_username
```

#### Step 2: Configure WSGI File

Edit your WSGI configuration file (e.g., `/var/www/yourusername_pythonanywhere_com_wsgi.py`):

```python
import sys
import os
from dotenv import load_dotenv

# Add your project directory to the sys.path
project_home = '/home/yourusername/Weather-Monitoring-System'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Load environment variables
load_dotenv(os.path.join(project_home, '.env'))

# Import your Flask app
from app import app as application
```

#### Step 3: Configure GitHub Actions Secrets

Add these secrets to your GitHub repository (Settings → Secrets and variables → Actions):

- `WEBHOOK_SECRET`: Same as `GITHUB_WEBHOOK_SECRET` in your `.env`
- `PYTHONANYWHERE_WEBHOOK_URL`: `https://yourusername.pythonanywhere.com/github-webhook`

Every push to `master` or `main` will trigger the GitHub Actions workflow which sends a POST request to your deployment endpoint.

#### Step 4: Keep Your App Alive

Set up [PythonAnywhere-Auto-Renew](https://github.com/tanishqmudaliar/PythonAnywhere-Auto-Renew) to prevent your free tier app from expiring every 90 days.

---

## API Reference

### Weather Endpoints

| Endpoint               | Method | Parameters   | Description                      |
| ---------------------- | ------ | ------------ | -------------------------------- |
| `/`                    | GET    | —            | Main application page            |
| `/api/current-weather` | GET    | `location`   | Current weather data             |
| `/api/forecast`        | GET    | `location`   | 5-day / 3-hour forecast          |
| `/api/air-quality`     | GET    | `location`   | Air quality index and pollutants |
| `/api/reverse-geocode` | GET    | `lat`, `lon` | City name from coordinates       |

### Deployment Endpoint

| Endpoint          | Method | Description                                                              |
| ----------------- | ------ | ------------------------------------------------------------------------ |
| `/github-webhook` | POST   | Receives deployment request from GitHub Actions, pulls code, reloads app |
| `/deployment-log` | GET    | View deployment log (debugging)                                          |

### Example Request

```bash
curl "https://tanishqmudaliar.pythonanywhere.com/api/current-weather?location=Mumbai"
```

### Example Response

```json
{
  "clouds": 0,
  "description": "Haze",
  "feels_like": 25.99,
  "humidity": 65,
  "icon": "50n",
  "weather_id": 721,
  "weather_main": "Haze",
  "location": "Mumbai, IN",
  "pressure": 1014,
  "pressure_sea_level": 1014,
  "pressure_grnd_level": 1013,
  "rain_1h": 0,
  "snow_1h": 0,
  "sunrise": 1769305456,
  "sunset": 1769345828,
  "temp_max": 25.99,
  "temp_min": 25.99,
  "temperature": 25.99,
  "timestamp": 1769351532,
  "timezone": 19800,
  "uv_index": 0.0,
  "visibility": 2500,
  "wind_direction": 300,
  "wind_gust": 2.57,
  "wind_speed": 2.57
}
```

---

## Project Structure

```
Weather-Monitoring-System/
├── .github/
│   ├── logs/                   # Deployment logs (gitignored)
│   └── workflows/
│       └── deploy.yml          # CI/CD workflow
├── static/
│   ├── app.js                  # Frontend JavaScript
│   ├── styles.css              # CSS styling
│   └── favicon.ico             # Website icon
├── templates/
│   └── index.html              # Main HTML template
├── app.py                      # Flask backend + webhook endpoint
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container configuration
├── docker-compose.yml          # Docker Compose orchestration
├── .dockerignore              # Docker ignore rules
├── .env                        # Environment variables (gitignored)
├── .env.example               # Environment template
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
└── README.md                   # Project documentation
```

---

## Configuration

### Environment Variables

| Variable                   | Description                               | Required       |
| -------------------------- | ----------------------------------------- | -------------- |
| `OPENWEATHER_API_KEY`      | OpenWeatherMap API key                    | Yes            |
| `GITHUB_WEBHOOK_SECRET`    | Secret for webhook signature verification | For deployment |
| `PYTHONANYWHERE_API_TOKEN` | PythonAnywhere API token                  | For deployment |
| `PYTHONANYWHERE_USERNAME`  | Your PythonAnywhere username              | For deployment |

### API Rate Limits

OpenWeatherMap free tier limits:

- 60 calls/minute
- 1,000,000 calls/month

---

## Usage

### Search for a City

1. Enter a city name in the search box
2. Click the search button or press Enter
3. View current weather and forecast data

### Use Geolocation

1. Click the location button (map marker icon)
2. Allow browser location access when prompted
3. Weather data for your current location will load automatically

### Switch Temperature Units

- Click **°C** for Celsius (Metric)
- Click **°F** for Fahrenheit (Imperial)
- All values update automatically

### View Forecast

1. Click the **Forecast** tab
2. View the temperature trend chart
3. Scroll through daily forecast cards

---

## Related Repositories

| Repository                                                                                | Purpose                          |
| ----------------------------------------------------------------------------------------- | -------------------------------- |
| [Weather-Monitoring-System](https://github.com/tanishqmudaliar/Weather-Monitoring-System) | Main application (this repo)     |
| [PythonAnywhere-Auto-Renew](https://github.com/tanishqmudaliar/PythonAnywhere-Auto-Renew) | Keeps the app alive on free tier |

Together, these repositories provide:

- Instant automated deployment on every push
- 24/7 uptime with auto-renewal bot
- Zero-maintenance hosting solution

---

## Troubleshooting

### "No OpenWeather API key found"

Ensure your `.env` file exists in the project root with a valid API key:

```env
OPENWEATHER_API_KEY=your_actual_api_key
```

### Location Not Found

- Check spelling of the city name
- Try adding a country code (e.g., "London,UK")
- Verify your internet connection

### Geolocation Not Working

- Allow location access in browser settings
- Use HTTPS or localhost
- Check browser console for errors

### Deployment Not Triggering

- Verify GitHub Actions secrets (`WEBHOOK_SECRET`, `PYTHONANYWHERE_WEBHOOK_URL`) are set correctly
- Check GitHub Actions workflow runs in the Actions tab
- Ensure PythonAnywhere API token is valid
- Review deployment logs at `/deployment-log`

### Docker Issues

**"docker: command not found"**

- Install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop/)
- Ensure Docker Desktop is running

**Container keeps restarting**

```bash
# Check what's wrong
docker compose logs weather-app

# Common issues:
# 1. Missing or invalid OPENWEATHER_API_KEY in .env
# 2. Port 5000 already in use (change port in docker-compose.yml)
# 3. Syntax error in .env file
```

**Changes to code not reflecting**

```bash
# Rebuild the container
docker compose down
docker compose up --build -d
```

**Need to see what's happening inside the container?**

```bash
# Access container shell
docker compose exec weather-app /bin/bash

# Or just view logs
docker compose logs -f weather-app
```

---

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

## Credits

**Development Team:**

- Tanishq Mudaliar
- Hrshita Balakrishnan
- Saivel Konar
- Pranali Raut

**Acknowledgments:**

- [OpenWeatherMap](https://openweathermap.org/) — Weather data provider
- [Open-Meteo](https://open-meteo.com/) — UV index data
- [Chart.js](https://www.chartjs.org/) — Data visualization
- [Font Awesome](https://fontawesome.com/) — Icons
- [PythonAnywhere](https://www.pythonanywhere.com/) — Hosting platform
- [Docker](https://www.docker.com/) — Containerization platform

---

Made with ❤️ by [Tanishq Mudaliar](https://github.com/tanishqmudaliar)

**Stop tab-hopping for the forecast. One dashboard, every metric that matters. ⛅**
