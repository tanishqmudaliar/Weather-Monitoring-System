# Weather Monitoring System

A modern, responsive web application for monitoring real-time weather conditions and forecasts powered by the OpenWeatherMap API.

![Python](https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?logo=flask&logoColor=white)
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
  - [Local Development](#local-development)
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
- UV index via Open-Meteo API integration
- Sunrise/sunset times with timezone support
- Air quality index (AQI) with pollutant breakdown

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
- Zero-downtime automated deployment via GitHub webhooks
- Deployment logging with Git-backed audit trail
- Auto-renewal integration for free-tier hosting

---

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| **Backend** | Python 3.14, Flask 3.0.0 |
| **Frontend** | HTML5, CSS3, JavaScript (ES6+), Chart.js |
| **APIs** | OpenWeatherMap, Open-Meteo (UV Index) |
| **Deployment** | PythonAnywhere, GitHub Webhooks |
| **CI/CD** | GitHub Actions |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FULLY AUTOMATED PYTHONANYWHERE HOSTING                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                              GITHUB                                  │   │
│  │                                                                      │   │
│  │   ┌─────────────────────────────┐  ┌─────────────────────────────┐  │   │
│  │   │  Weather-Monitoring-System  │  │  PythonAnywhere-Auto-Renew  │  │   │
│  │   │                             │  │                             │  │   │
│  │   │  • Main application code   │  │  • Renewal bot              │  │   │
│  │   │  • Webhook endpoint        │  │  • Runs 1st & 15th monthly  │  │   │
│  │   │  • Auto-deploys on push    │  │  • Keeps app alive forever  │  │   │
│  │   └──────────────┬──────────────┘  └──────────────┬──────────────┘  │   │
│  │                  │                                │                  │   │
│  │                  │ Webhook                        │ GitHub Actions   │   │
│  │                  ▼                                ▼                  │   │
│  └──────────────────┼────────────────────────────────┼──────────────────┘   │
│                     │                                │                      │
│  ┌──────────────────▼────────────────────────────────▼──────────────────┐   │
│  │                         PYTHONANYWHERE                                │   │
│  │                                                                       │   │
│  │   ┌─────────────────────────┐    ┌─────────────────────────┐         │   │
│  │   │    Webhook Receiver     │    │     Auto-Renewal        │         │   │
│  │   │  • git pull             │    │  • Extends app expiry   │         │   │
│  │   │  • pip install          │    │  • Prevents shutdown    │         │   │
│  │   │  • Reload webapp        │    │  • Zero maintenance     │         │   │
│  │   └─────────────────────────┘    └─────────────────────────┘         │   │
│  │                                                                       │   │
│  │            https://tanishqmudaliar.pythonanywhere.com                │   │
│  └───────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│           Push code → Instantly live → Stays alive forever                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Deployment Flow

1. Push code to `master` branch
2. GitHub sends webhook POST to `/github-webhook`
3. Flask endpoint pulls latest code via `git pull`
4. Dependencies are installed with `pip install -r requirements.txt`
5. PythonAnywhere API reloads the webapp
6. Changes are live within seconds

---

## Getting Started

### Prerequisites

- Python 3.8+ (developed with 3.14)
- OpenWeatherMap API key ([Get one free](https://home.openweathermap.org/api_keys))

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/tanishqmudaliar/Weather-Monitoring-System.git
   cd Weather-Monitoring-System
   ```

2. **Create and activate a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
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

### PythonAnywhere Deployment

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

#### Step 2: Configure GitHub Webhook

1. Go to your repository → **Settings** → **Webhooks** → **Add webhook**
2. Configure:
   - **Payload URL**: `https://yourusername.pythonanywhere.com/github-webhook`
   - **Content type**: `application/json`
   - **Secret**: Same as `GITHUB_WEBHOOK_SECRET` in your `.env`
   - **Events**: Just the push event
3. Save the webhook

#### Step 3: Keep Your App Alive

Set up [PythonAnywhere-Auto-Renew](https://github.com/tanishqmudaliar/PythonAnywhere-Auto-Renew) to prevent your free tier app from expiring every 90 days.

---

## API Reference

### Weather Endpoints

| Endpoint | Method | Parameters | Description |
|----------|--------|------------|-------------|
| `/` | GET | — | Main application page |
| `/api/current-weather` | GET | `location` | Current weather data |
| `/api/forecast` | GET | `location` | 5-day / 3-hour forecast |
| `/api/air-quality` | GET | `location` | Air quality index and pollutants |
| `/api/reverse-geocode` | GET | `lat`, `lon` | City name from coordinates |

### Deployment Endpoint

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/github-webhook` | POST | Receives GitHub webhook, pulls code, reloads app |
| `/deployment-log` | GET | View deployment log (debugging) |

### Example Request

```bash
curl "https://tanishqmudaliar.pythonanywhere.com/api/current-weather?location=Mumbai"
```

### Example Response

```json
{
  "location": "Mumbai, IN",
  "temperature": 28.5,
  "feels_like": 32.1,
  "description": "Partly Cloudy",
  "humidity": 78,
  "pressure": 1012,
  "wind_speed": 3.5,
  "uv_index": 6.2,
  "sunrise": 1706150400,
  "sunset": 1706191200
}
```

---

## Project Structure

```
Weather-Monitoring-System/
├── .github/
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
├── .env                        # Environment variables (not in git)
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
└── README.md                   # Project documentation
```

---

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | Yes |
| `GITHUB_WEBHOOK_SECRET` | Secret for webhook signature verification | For deployment |
| `PYTHONANYWHERE_API_TOKEN` | PythonAnywhere API token | For deployment |
| `PYTHONANYWHERE_USERNAME` | Your PythonAnywhere username | For deployment |

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

| Repository | Purpose |
|------------|---------|
| [Weather-Monitoring-System](https://github.com/tanishqmudaliar/Weather-Monitoring-System) | Main application (this repo) |
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

### Webhook Not Triggering Deployment
- Verify webhook secret matches in GitHub and `.env`
- Check webhook delivery status in GitHub Settings → Webhooks
- Ensure PythonAnywhere API token is valid
- Review deployment logs at `/deployment-log`

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

---

Made with ❤️ by the Weather Monitoring System Team