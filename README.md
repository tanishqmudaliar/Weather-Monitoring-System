# Weather Monitoring System

A modern, responsive web application for monitoring real-time weather conditions and forecasts powered by the OpenWeatherMap API. 

![Weather Monitoring System](https://img.shields.io/badge/Python-3.14-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Auto Deploy](https://img.shields.io/badge/Deploy-Automated-brightgreen.svg)
![PythonAnywhere](https://img.shields.io/badge/Hosted-PythonAnywhere-orange.svg)

## Features

### Current Weather
- **Real-time Weather Data**: Get current weather conditions for any city worldwide
- **Comprehensive Details**: View temperature, feels-like temperature, humidity, pressure, wind speed, and direction
- **Sunrise/Sunset Times**: Track daylight hours for your location
- **Weather Icons**: Visual representation of current weather conditions

### 5-Day Forecast
- **Extended Forecast**: View weather predictions for the next 5 days
- **Interactive Charts**: Temperature trends displayed using Chart.js
- **Daily Summaries**: Average temperature and humidity for each day
- **Visual Weather Cards**: Easy-to-read forecast cards with icons

### User Interface
- **Unit Toggle**: Switch between Metric (°C) and Imperial (°F) units
- **Geolocation Support**: Automatically detect your current location
- **Responsive Design**:  Optimized for desktop, tablet, and mobile devices
- **Tab Navigation**: Switch between current weather and forecast views
- **Modern UI**: Clean, intuitive interface with Font Awesome icons

## Tech Stack

### Backend
- **Python 3.14**:  Core programming language
- **Flask**: Web framework for handling API requests and routing
- **Requests**: HTTP library for API calls
- **python-dotenv**: Environment variable management

### Frontend
- **HTML5**: Semantic markup
- **CSS3**:  Modern styling with CSS variables and flexbox/grid
- **JavaScript (ES6+)**: Interactive functionality
- **Chart. js**: Data visualization for forecast charts
- **Font Awesome**: Icon library

### API
- **OpenWeatherMap API**: Weather data provider

### Deployment & Infrastructure
- **PythonAnywhere**: Cloud hosting platform
- **GitHub Webhooks**: Automated deployment on push
- **GitHub Actions**: CI/CD pipeline integration

## 🚀 Automated Deployment

This project features **fully automated deployment** - every push to `master` automatically deploys to PythonAnywhere! 

### How It Works

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────────────────┐
│  Push to        │ ---> │  GitHub sends   │ ---> │  Flask webhook endpoint     │
│  master branch  │ ---> │  webhook POST   │ ---> │  pulls code & reloads app   │
└─────────────────┘      └─────────────────┘      └─────────────────────────────┘
```

### Deployment Architecture

| Component | Purpose |
|-----------|---------|
| **GitHub Webhook** | Triggers deployment on every push to master |
| **`/github-webhook` endpoint** | Receives webhook, runs `git pull`, reloads app |
| **PythonAnywhere API** | Reloads the webapp after code update |
| **[PythonAnywhere-Auto-Renew](https://github.com/tanishqmudaliar/PythonAnywhere-Auto-Renew)** | Keeps the free tier app alive forever |

### Zero-Downtime Deployment

1. ✅ Push code to GitHub
2. ✅ Webhook automatically triggers
3. ✅ Code is pulled on PythonAnywhere
4. ✅ Dependencies are installed
5. ✅ Webapp reloads with new code
6. ✅ Live in seconds! 

## Installation

### Prerequisites
- Python 3.14 installed on your system
- OpenWeatherMap API key ([Get one for free](https://home.openweathermap.org/api_keys))

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/tanishqmudaliar/Weather-Monitoring-System.git
   cd Weather-Monitoring-System
   ```

2. **Install required Python packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file in the project root**
   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```
   Replace `your_api_key_here` with your actual OpenWeatherMap API key.

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://127.0.0.1:5000`

### PythonAnywhere Deployment Setup

#### Step 1: Initial Setup on PythonAnywhere

1. Create a free account at [pythonanywhere.com](https://www.pythonanywhere.com)
2. Open a Bash console and clone the repo:
   ```bash
   git clone https://github.com/tanishqmudaliar/Weather-Monitoring-System.git
   ```
3. Set up your web app pointing to the cloned directory
4. Create a `.env` file with your secrets:
   ```env
   OPENWEATHER_API_KEY=your_openweather_key
   GITHUB_WEBHOOK_SECRET=your_random_secret
   PYTHONANYWHERE_API_TOKEN=your_api_token
   PYTHONANYWHERE_USERNAME=your_username
   ```

#### Step 2: Configure GitHub Webhook

1. Go to your repo → **Settings** → **Webhooks** → **Add webhook**
2. Configure: 
   - **Payload URL**: `https://yourusername.pythonanywhere.com/github-webhook`
   - **Content type**: `application/json`
   - **Secret**: Same as `GITHUB_WEBHOOK_SECRET` in your `.env`
   - **Events**: Just the push event
3. Save the webhook

#### Step 3: Keep Your App Alive

Use [PythonAnywhere-Auto-Renew](https://github.com/tanishqmudaliar/PythonAnywhere-Auto-Renew) to prevent your free tier app from expiring. 

## Project Structure

```
Weather-Monitoring-System/
│
├── . github/
│   └── workflows/
│       └── deploy.yml      # CI/CD workflow
│
├── app.py                  # Flask backend server + webhook endpoint
├── .env                    # Environment variables (not in git)
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
│
├── templates/
│   └── index.html          # Main HTML template
│
└── static/
    ├── app.js              # JavaScript functionality
    ├── styles.css          # CSS styling
    └── favicon.ico         # Website icon
```

## API Endpoints

### Application Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serves the main application page |
| `/api/current-weather` | GET | Current weather data (param: `location`) |
| `/api/forecast` | GET | 5-day weather forecast (param: `location`) |
| `/api/reverse-geocode` | GET | City name from coordinates (params: `lat`, `lon`) |

### Deployment Endpoint

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/github-webhook` | POST | Receives GitHub webhook, pulls code, reloads app |

## Usage

### Search for a City
1. Enter a city name in the search box
2. Click the search button or press Enter
3. View current weather and forecast data

### Use Your Location
1. Click the location button (map marker icon)
2. Allow browser location access when prompted
3. Weather data for your location will be displayed automatically

### Switch Temperature Units
- Click the °C button for Celsius (Metric)
- Click the °F button for Fahrenheit (Imperial)
- All temperature values update automatically

### View Forecast
1. Click the "Forecast" tab
2. View the temperature trend chart
3. Scroll through daily forecast cards

## 🔗 Related Repositories

| Repository | Purpose |
|------------|---------|
| **[Weather-Monitoring-System](https://github.com/tanishqmudaliar/Weather-Monitoring-System)** | Main application (this repo) |
| **[PythonAnywhere-Auto-Renew](https://github.com/tanishqmudaliar/PythonAnywhere-Auto-Renew)** | Keeps the app alive on free tier |

Together, these repos provide: 
- ✅ **Instant automated deployment** on every push
- ✅ **24/7 uptime** with auto-renewal bot
- ✅ **Zero maintenance** hosting solution

## Dependencies

```
Flask==3.0.0
requests==2.31.0
python-dotenv==1.0.0
```

Install all dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `OPENWEATHER_API_KEY` | OpenWeatherMap API key | ✅ Yes |
| `GITHUB_WEBHOOK_SECRET` | Secret for webhook verification | ✅ For auto-deploy |
| `PYTHONANYWHERE_API_TOKEN` | PythonAnywhere API token | ✅ For auto-deploy |
| `PYTHONANYWHERE_USERNAME` | Your PythonAnywhere username | ✅ For auto-deploy |

### API Rate Limits
Free tier OpenWeatherMap accounts have the following limits:
- 60 calls per minute
- 1,000,000 calls per month

## Browser Support
- Chrome (recommended)
- Firefox
- Safari
- Edge
- Opera

Requires a modern browser with JavaScript enabled and geolocation support for location features.

## Troubleshooting

### "No OpenWeather API key found" Error
Make sure you have created a `.env` file in the project root with your API key:
```
OPENWEATHER_API_KEY=your_actual_api_key
```

### Location Not Found
- Check spelling of the city name
- Try adding country code (e.g., "London,UK")
- Ensure you have an active internet connection

### Geolocation Not Working
- Allow location access in browser settings
- Ensure you're using HTTPS or localhost
- Check browser console for specific errors

### Webhook Not Triggering Deployment
- Verify webhook secret matches in GitHub and `.env`
- Check webhook delivery status in GitHub Settings → Webhooks
- Ensure PythonAnywhere API token is valid
- Check PythonAnywhere error logs

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests. 

## Credits

**Development Team:**
- Tanishq Mudaliar
- Hrshita Balakrishnan
- Saivel Konar
- Pranali Raut

**Data Provider:** [OpenWeatherMap](https://openweathermap.org/)

## License

This project is open source and available under the MIT License.

## Acknowledgments

- OpenWeatherMap API for providing weather data
- Font Awesome for icons
- Chart.js for data visualization
- Flask framework for backend development
- PythonAnywhere for hosting

## Future Enhancements

Potential features for future versions:
- Historical weather data
- Weather alerts and notifications
- Multiple location comparison
- Extended 14-day forecast
- Weather maps and radar
- Save favorite locations
- Dark mode theme
- Weather statistics and analytics

## Contact

For questions or support, please contact the development team.

---

**Made with ❤️ by the Weather Monitoring System Team**

**🌐 [Live Demo](https://tanishqmudaliar.pythonanywhere.com) | 🔄 [Auto-Renew Bot](https://github.com/tanishqmudaliar/PythonAnywhere-Auto-Renew)**