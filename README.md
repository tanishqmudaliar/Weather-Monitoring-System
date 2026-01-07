# Weather Monitoring System

A modern, responsive web application for monitoring real-time weather conditions and forecasts powered by the OpenWeatherMap API.

![Weather Monitoring System](https://img.shields.io/badge/Python-3.14-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

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
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Tab Navigation**: Switch between current weather and forecast views
- **Modern UI**: Clean, intuitive interface with Font Awesome icons

## Tech Stack

### Backend
- **Python 3.14**: Core programming language
- **Flask**: Web framework for handling API requests and routing
- **Requests**: HTTP library for API calls
- **python-dotenv**: Environment variable management

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS variables and flexbox/grid
- **JavaScript (ES6+)**: Interactive functionality
- **Chart.js**: Data visualization for forecast charts
- **Font Awesome**: Icon library

### API
- **OpenWeatherMap API**: Weather data provider

## Installation

### Prerequisites
- Python 3.14 installed on your system
- OpenWeatherMap API key ([Get one for free](https://home.openweathermap.org/api_keys))

### Setup Steps

1. **Clone or download the repository**
   ```bash
   cd "Weather Monitoring System"
   ```

2. **Install required Python packages**
   ```bash
   pip install flask requests python-dotenv
   ```

3. **Create a `.env` file in the project root**
   ```
   OPENWEATHER_API_KEY=your_api_key_here
   ```
   Replace `your_api_key_here` with your actual OpenWeatherMap API key.

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://127.0.0.1:5000`

## Project Structure

```
Weather Monitoring System/
│
├── app.py                  # Flask backend server
├── .env                    # Environment variables (API key)
├── README.md              # Project documentation
│
├── templates/
│   └── index.html         # Main HTML template
│
└── static/
    ├── app.js             # JavaScript functionality
    ├── styles.css         # CSS styling
    └── favicon.ico        # Website icon
```

## API Endpoints

### `/`
- **Method**: GET
- **Description**: Serves the main application page

### `/api/current-weather`
- **Method**: GET
- **Parameters**: `location` (city name)
- **Response**: Current weather data including temperature, humidity, wind, etc.

### `/api/forecast`
- **Method**: GET
- **Parameters**: `location` (city name)
- **Response**: 5-day weather forecast with 3-hour intervals

### `/api/reverse-geocode`
- **Method**: GET
- **Parameters**: `lat` (latitude), `lon` (longitude)
- **Response**: City name from coordinates

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

## Features in Detail

### Temperature Conversion
The application supports seamless switching between Celsius and Fahrenheit units without requiring new API calls. All temperatures, including feels-like and forecast data, are converted instantly.

### Geolocation
Uses the browser's Geolocation API combined with OpenWeatherMap's reverse geocoding to automatically detect and display weather for your current location.

### Responsive Design
- Desktop: Full-width layout with multi-column grids
- Tablet: Adaptive grid that adjusts to screen size
- Mobile: Single-column layout optimized for touch interaction

### Error Handling
- Graceful error messages for invalid locations
- Network error handling
- API timeout protection
- User-friendly error notifications

## Dependencies

The project includes a `requirements.txt` file with all necessary dependencies:
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
The application requires the following environment variable:
- `OPENWEATHER_API_KEY`: Your OpenWeatherMap API key

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

