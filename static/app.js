// Professional Weather Intelligence Platform - JavaScript
let currentUnit = "metric";
let lastLocation = "";
let forecastChart = null;
let currentWeatherData = null;
let currentTimezoneOffset = 0; // Store city timezone offset

// DOM Elements
const locationInput = document.getElementById("location-input");
const searchBtn = document.getElementById("search-btn");
const geolocationBtn = document.getElementById("geolocation-btn");
const metricToggle = document.getElementById("metric-toggle");
const imperialToggle = document.getElementById("imperial-toggle");
const dashboard = document.getElementById("dashboard");
const loader = document.getElementById("loader");
const errorSection = document.getElementById("error-section");
const emptyState = document.getElementById("empty-state");

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  setupEventListeners();
  setInterval(() => updateCurrentTime(currentTimezoneOffset), 1000);
  if (emptyState) emptyState.style.display = "block";
});

function setupEventListeners() {
  if (searchBtn) searchBtn.addEventListener("click", handleSearch);

  if (locationInput) {
    locationInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") handleSearch();
    });
  }

  if (geolocationBtn) geolocationBtn.addEventListener("click", getUserLocation);
  if (metricToggle)
    metricToggle.addEventListener("click", () => changeUnit("metric"));
  if (imperialToggle)
    imperialToggle.addEventListener("click", () => changeUnit("imperial"));

  // Quick city chips
  const cityChips = document.querySelectorAll(".city-chip");
  cityChips.forEach((chip) => {
    chip.addEventListener("click", () => {
      const city = chip.getAttribute("data-city");
      if (city && locationInput) {
        locationInput.value = city;
        handleSearch();
      }
    });
  });
}

function updateCurrentTime(timezoneOffset = 0) {
  const timeEl = document.getElementById("current-time");
  if (!timeEl) return;

  const now = new Date();
  const utc = now.getTime() + now.getTimezoneOffset() * 60000;
  const localTime = new Date(utc + timezoneOffset * 1000);

  timeEl.textContent = localTime.toLocaleString("en-US", {
    weekday: "long",
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

function handleSearch() {
  const location = locationInput.value.trim();
  if (location) {
    lastLocation = location;
    fetchAllWeatherData(location);
  }
}

function getUserLocation() {
  if (!navigator.geolocation) {
    showError("Geolocation is not supported by your browser");
    return;
  }

  if (geolocationBtn) {
    geolocationBtn.disabled = true;
    geolocationBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
  }

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const lat = position.coords.latitude;
      const lon = position.coords.longitude;

      fetch(`/api/reverse-geocode?lat=${lat}&lon=${lon}`)
        .then((response) => {
          if (!response.ok) throw new Error("Reverse geocoding failed");
          return response.json();
        })
        .then((data) => {
          const city = data && data.city ? data.city : "";
          if (city) {
            locationInput.value = city;
            lastLocation = city;
            fetchAllWeatherData(city);
          } else {
            showError("Could not determine location");
          }
        })
        .catch((error) => {
          console.error("Error in reverse geocoding:", error);
          showError("Failed to get your location");
        })
        .finally(() => {
          if (geolocationBtn) {
            geolocationBtn.disabled = false;
            geolocationBtn.innerHTML =
              '<i class="fas fa-location-crosshairs"></i>';
          }
        });
    },
    (error) => {
      console.error("Geolocation error:", error);
      if (geolocationBtn) {
        geolocationBtn.disabled = false;
        geolocationBtn.innerHTML = '<i class="fas fa-location-crosshairs"></i>';
      }
      showError("Failed to get your location");
    },
  );
}

function changeUnit(unit) {
  if (currentUnit === unit) return;

  currentUnit = unit;
  if (metricToggle) metricToggle.classList.toggle("active", unit === "metric");
  if (imperialToggle)
    imperialToggle.classList.toggle("active", unit === "imperial");

  // Update all temperature displays
  updateTemperatureDisplays();

  // Refresh data if we have a location
  if (lastLocation) {
    fetchAllWeatherData(lastLocation);
  }
}

function updateTemperatureDisplays() {
  const tempUnits = document.querySelectorAll(
    ".temp-unit, #temp-unit, #feels-unit",
  );
  tempUnits.forEach((el) => {
    el.textContent = currentUnit === "metric" ? "°C" : "°F";
  });
}

async function fetchAllWeatherData(location) {
  showLoading();

  try {
    // Fetch all data in parallel
    const [currentWeather, forecast, airQuality] = await Promise.all([
      fetchCurrentWeather(location),
      fetchForecast(location),
      fetchAirQuality(location),
    ]);

    if (currentWeather) {
      displayCurrentWeather(currentWeather);
      displayWeatherAlerts(currentWeather);
      currentWeatherData = currentWeather;
    }

    if (forecast) {
      displayHourlyForecast(forecast);
      displayDailyForecast(forecast);
      createTemperatureChart(forecast);
    }

    if (airQuality) {
      displayAirQuality(airQuality);
    }

    hideLoading();
    showDashboard();
  } catch (error) {
    console.error("Error fetching weather data:", error);
    hideLoading();
    showError("Failed to fetch weather data");
  }
}

async function fetchCurrentWeather(location) {
  try {
    const response = await fetch(
      `/api/current-weather?location=${encodeURIComponent(location)}`,
    );
    if (!response.ok) throw new Error("Failed to fetch current weather");
    return await response.json();
  } catch (error) {
    console.error("Error fetching current weather:", error);
    return null;
  }
}

async function fetchForecast(location) {
  try {
    const response = await fetch(
      `/api/forecast?location=${encodeURIComponent(location)}`,
    );
    if (!response.ok) throw new Error("Failed to fetch forecast");
    return await response.json();
  } catch (error) {
    console.error("Error fetching forecast:", error);
    return null;
  }
}

async function fetchAirQuality(location) {
  try {
    const response = await fetch(
      `/api/air-quality?location=${encodeURIComponent(location)}`,
    );
    if (!response.ok) return null;
    return await response.json();
  } catch (error) {
    console.error("Error fetching air quality:", error);
    return null;
  }
}

function displayCurrentWeather(data) {
  // Location
  const locationName = document.getElementById("location-name");
  const countryCode = document.getElementById("country-code");
  if (locationName) {
    const parts = data.location.split(", ");
    locationName.textContent = parts[0] || data.location;
    if (countryCode && parts[1]) countryCode.textContent = parts[1];
  }

  // Weather Icon
  const weatherIcon = document.getElementById("weather-icon");
  if (weatherIcon && data.icon) {
    weatherIcon.src = `https://openweathermap.org/img/wn/${data.icon}@4x.png`;
    weatherIcon.alt = data.description;
  }

  // Temperature
  const tempC = parseFloat(data.temperature);
  const tempF = (tempC * 9) / 5 + 32;
  const currentTemp = document.getElementById("current-temp");
  if (currentTemp) {
    currentTemp.textContent =
      currentUnit === "metric" ? tempC.toFixed(1) : tempF.toFixed(1);
  }

  // Feels Like
  const feelsC = parseFloat(data.feels_like);
  const feelsF = (feelsC * 9) / 5 + 32;
  const feelsLike = document.getElementById("feels-like");
  if (feelsLike) {
    feelsLike.textContent =
      currentUnit === "metric" ? feelsC.toFixed(1) : feelsF.toFixed(1);
  }

  // Description
  const weatherDesc = document.getElementById("weather-desc");
  if (weatherDesc) weatherDesc.textContent = data.description;

  // Stats
  updateStat("humidity", `${data.humidity}%`);
  updateStat("pressure", `${data.pressure} hPa`);
  updateStat("pressure-sea", `${data.pressure_sea_level || data.pressure} hPa`);
  updateStat(
    "pressure-grnd",
    `${data.pressure_grnd_level || data.pressure} hPa`,
  );

  const windMps = parseFloat(data.wind_speed);
  const windMph = windMps * 2.237;
  updateStat(
    "wind-speed",
    currentUnit === "metric"
      ? `${windMps.toFixed(1)} m/s`
      : `${windMph.toFixed(1)} mph`,
  );

  updateStat("visibility", `${(data.visibility / 1000).toFixed(1)} km`);
  updateStat("clouds", `${data.clouds}%`);

  // Wind Direction with compass
  const windDeg = data.wind_direction || 0;
  const directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"];
  const dirIndex = Math.round(windDeg / 45) % 8;
  updateStat("wind-direction", `${directions[dirIndex]} ${windDeg}°`);

  // High/Low Temperature
  const minC = parseFloat(data.temp_min);
  const maxC = parseFloat(data.temp_max);
  const minF = (minC * 9) / 5 + 32;
  const maxF = (maxC * 9) / 5 + 32;
  const minTemp = currentUnit === "metric" ? minC.toFixed(0) : minF.toFixed(0);
  const maxTemp = currentUnit === "metric" ? maxC.toFixed(0) : maxF.toFixed(0);
  updateStat("temp-range", `${maxTemp}° / ${minTemp}°`);

  // UV Index - Now from Open-Meteo API
  updateStat("uv-index", data.uv_index !== undefined ? data.uv_index : "N/A");

  // Sun & Moon
  if (data.sunrise && data.sunset) {
    const sunrise = new Date(data.sunrise * 1000);
    const sunset = new Date(data.sunset * 1000);

    updateStat(
      "sunrise",
      sunrise.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    );
    updateStat(
      "sunset",
      sunset.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    );

    updateDaylightProgress(sunrise, sunset);
  }

  if (data.timezone !== undefined) {
    currentTimezoneOffset = data.timezone;
    updateCurrentTime(data.timezone);
  }
}

function updateStat(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

function updateDaylightProgress(sunrise, sunset) {
  const now = new Date();
  const totalDaylight = sunset - sunrise;
  const elapsed = now - sunrise;
  const percentage = Math.max(
    0,
    Math.min(100, (elapsed / totalDaylight) * 100),
  );

  const progress = document.getElementById("daylight-progress");
  const indicator = document.getElementById("daylight-indicator");
  const hours = document.getElementById("daylight-hours");

  if (progress) progress.style.width = `${percentage}%`;
  if (indicator) indicator.style.left = `${percentage}%`;
  if (hours) {
    const daylightHours = totalDaylight / (1000 * 60 * 60);
    hours.textContent = `${daylightHours.toFixed(1)} hours`;
  }
}

function displayAirQuality(data) {
  if (!data || !data.aqi) return;

  const aqiValue = document.getElementById("aqi-value");
  const aqiStatus = document.getElementById("aqi-status");
  const aqiDescription = document.getElementById("aqi-description");
  const aqiCircle = document.getElementById("aqi-circle");

  if (aqiValue) aqiValue.textContent = data.aqi;

  let status = "Good";
  let description = "Air quality is satisfactory";
  let colorClass = "aqi-good";

  if (data.aqi <= 50) {
    status = "Good";
    description = "Air quality is excellent";
    colorClass = "aqi-good";
  } else if (data.aqi <= 100) {
    status = "Moderate";
    description = "Air quality is acceptable";
    colorClass = "aqi-moderate";
  } else if (data.aqi <= 150) {
    status = "Unhealthy for Sensitive";
    description = "Sensitive groups may be affected";
    colorClass = "aqi-unhealthy-sensitive";
  } else if (data.aqi <= 200) {
    status = "Unhealthy";
    description = "Everyone may experience effects";
    colorClass = "aqi-unhealthy";
  } else if (data.aqi <= 300) {
    status = "Very Unhealthy";
    description = "Health warnings of emergency conditions";
    colorClass = "aqi-very-unhealthy";
  } else {
    status = "Hazardous";
    description = "Health alert: everyone may experience serious effects";
    colorClass = "aqi-hazardous";
  }

  if (aqiStatus) aqiStatus.textContent = status;
  if (aqiDescription) aqiDescription.textContent = description;
  if (aqiCircle) {
    aqiCircle.className = `aqi-circle ${colorClass}`;
  }

  // Update pollutant values
  updateStat("pm25", data.pm25 ? data.pm25.toFixed(1) : "--");
  updateStat("pm10", data.pm10 ? data.pm10.toFixed(1) : "--");
  updateStat("o3", data.o3 ? data.o3.toFixed(1) : "--");
  updateStat("no2", data.no2 ? data.no2.toFixed(1) : "--");
  updateStat("no", data.no ? data.no.toFixed(1) : "--");
  updateStat("nh3", data.nh3 ? data.nh3.toFixed(1) : "--");
}

function displayHourlyForecast(data) {
  const container = document.getElementById("hourly-forecast");
  if (!container) return;

  container.innerHTML = "";
  const hourlyData = data.slice(0, 16); // 48 hours / 3-hour intervals = 16 items

  hourlyData.forEach((item) => {
    const date = new Date(item.dt * 1000);
    const tempC = parseFloat(item.temp);
    const tempF = (tempC * 9) / 5 + 32;
    const temp = currentUnit === "metric" ? tempC : tempF;

    const hourlyItem = document.createElement("div");
    hourlyItem.className = "hourly-item";
    hourlyItem.innerHTML = `
            <div class="hourly-time">${date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</div>
            <img src="https://openweathermap.org/img/wn/${item.icon}@2x.png" alt="${item.description}">
            <div class="hourly-temp">${temp.toFixed(1)}°</div>
            <div class="hourly-desc">${item.description}</div>
        `;
    container.appendChild(hourlyItem);
  });
}

function displayDailyForecast(data) {
  const container = document.getElementById("daily-forecast");
  if (!container) return;

  container.innerHTML = "";

  // Group by day
  const dailyData = {};
  data.forEach((item) => {
    const date = new Date(item.dt * 1000);
    const dateStr = date.toLocaleDateString();

    if (!dailyData[dateStr]) {
      dailyData[dateStr] = {
        date: date,
        temps: [],
        descriptions: [],
        icons: [],
        humidity: [],
      };
    }

    dailyData[dateStr].temps.push(parseFloat(item.temp));
    dailyData[dateStr].descriptions.push(item.description);
    dailyData[dateStr].icons.push(item.icon);
    dailyData[dateStr].humidity.push(item.humidity);
  });

  // Create daily cards (max 5 days)
  Object.keys(dailyData)
    .slice(0, 5)
    .forEach((dateStr) => {
      const day = dailyData[dateStr];
      const maxTempC = Math.max(...day.temps);
      const minTempC = Math.min(...day.temps);
      const maxTempF = (maxTempC * 9) / 5 + 32;
      const minTempF = (minTempC * 9) / 5 + 32;

      const maxTemp = currentUnit === "metric" ? maxTempC : maxTempF;
      const minTemp = currentUnit === "metric" ? minTempC : minTempF;

      const mostCommonIcon = day.icons[0];
      const mostCommonDesc = day.descriptions[0];

      const dailyItem = document.createElement("div");
      dailyItem.className = "daily-item";
      dailyItem.innerHTML = `
            <div class="daily-date">
                <div class="daily-weekday">${day.date.toLocaleDateString("en-US", { weekday: "short" })}</div>
                <div>${day.date.toLocaleDateString("en-US", { month: "short", day: "numeric" })}</div>
            </div>
            <div class="daily-icon">
                <img src="https://openweathermap.org/img/wn/${mostCommonIcon}@2x.png" alt="${mostCommonDesc}">
                <div class="daily-desc">${mostCommonDesc}</div>
            </div>
            <div class="temp-bar-container">
                <div class="temp-range">
                    <div class="temp-range-fill" style="left: 20%; width: 60%;"></div>
                </div>
            </div>
            <div class="temp-values">
                <span class="temp-max">${maxTemp.toFixed(0)}°</span>
                <span class="temp-min">${minTemp.toFixed(0)}°</span>
            </div>
        `;
      container.appendChild(dailyItem);
    });
}

function createTemperatureChart(data) {
  const canvas = document.getElementById("temp-chart");
  if (!canvas) return;

  if (forecastChart) {
    forecastChart.destroy();
  }

  const labels = [];
  const temperatures = [];
  const feelsLike = [];

  data.slice(0, 16).forEach((item) => {
    const date = new Date(item.dt * 1000);
    labels.push(
      date.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        hour: "2-digit",
      }),
    );

    const tempC = parseFloat(item.temp);
    const feelsC = parseFloat(item.feels_like);
    const temp = currentUnit === "metric" ? tempC : (tempC * 9) / 5 + 32;
    const feels = currentUnit === "metric" ? feelsC : (feelsC * 9) / 5 + 32;

    temperatures.push(temp);
    feelsLike.push(feels);
  });

  const ctx = canvas.getContext("2d");
  forecastChart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Temperature",
          data: temperatures,
          borderColor: "#60a5fa",
          backgroundColor: "rgba(96, 165, 250, 0.1)",
          borderWidth: 3,
          tension: 0.4,
          fill: true,
          pointRadius: 5,
          pointHoverRadius: 7,
          pointBackgroundColor: "#60a5fa",
          pointBorderColor: "#0a0e27",
          pointBorderWidth: 2,
        },
        {
          label: "Feels Like",
          data: feelsLike,
          borderColor: "#a78bfa",
          backgroundColor: "rgba(167, 139, 250, 0.1)",
          borderWidth: 2,
          borderDash: [8, 4],
          tension: 0.4,
          fill: false,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: "#a78bfa",
          pointBorderColor: "#0a0e27",
          pointBorderWidth: 2,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        intersect: false,
        mode: "index",
      },
      plugins: {
        legend: {
          labels: {
            color: "#cbd5e1",
            font: {
              size: 13,
              weight: "600",
              family: "'Space Grotesk', sans-serif",
            },
            padding: 20,
            usePointStyle: true,
            pointStyle: "circle",
          },
        },
        tooltip: {
          backgroundColor: "rgba(10, 14, 39, 0.95)",
          titleColor: "#f8fafc",
          bodyColor: "#cbd5e1",
          borderColor: "#60a5fa",
          borderWidth: 2,
          padding: 16,
          displayColors: true,
          titleFont: {
            size: 14,
            weight: "bold",
          },
          bodyFont: {
            size: 13,
          },
          callbacks: {
            label: function (context) {
              return ` ${context.dataset.label}: ${context.parsed.y.toFixed(1)}°`;
            },
          },
        },
      },
      scales: {
        x: {
          grid: {
            color: "rgba(148, 163, 184, 0.08)",
            drawBorder: false,
          },
          ticks: {
            color: "#64748b",
            font: {
              size: 11,
              weight: "500",
            },
            maxRotation: 45,
            minRotation: 0,
          },
        },
        y: {
          grid: {
            color: "rgba(148, 163, 184, 0.08)",
            drawBorder: false,
          },
          ticks: {
            color: "#64748b",
            font: {
              size: 11,
              weight: "500",
            },
            callback: (value) => `${value}°`,
          },
        },
      },
    },
  });
}

function showLoading() {
  if (loader) loader.classList.remove("hidden");
  if (dashboard) dashboard.classList.add("hidden");
  if (errorSection) errorSection.classList.add("hidden");
  if (emptyState) emptyState.style.display = "none";
}

function hideLoading() {
  if (loader) loader.classList.add("hidden");
}

function showDashboard() {
  if (emptyState) emptyState.style.display = "none";
  dashboard.classList.remove("hidden");
}

function showError(message) {
  hideLoading();
  if (dashboard) dashboard.classList.add("hidden");
  if (emptyState) emptyState.style.display = "none";
  if (errorSection) {
    errorSection.classList.remove("hidden");
    const errorText = errorSection.querySelector("p");
    if (errorText && message) errorText.textContent = message;
  }
}

function displayWeatherAlerts(data) {
  const alertsContainer = document.getElementById("weather-alerts");
  if (!alertsContainer) return;

  alertsContainer.innerHTML = "";

  const weatherId = data.weather_id;
  const weatherMain = data.weather_main;

  if (!weatherId) return;

  let alert = null;

  // Thunderstorm (200-299)
  if (weatherId >= 200 && weatherId < 300) {
    alert = {
      type: "danger",
      icon: "bolt",
      title: "Thunderstorm Warning",
      message: `${weatherMain}: ${data.description}. Seek shelter immediately.`,
    };
  }
  // Heavy Rain (502, 503, 504, 522)
  else if ([502, 503, 504, 522].includes(weatherId)) {
    alert = {
      type: "warning",
      icon: "cloud-showers-heavy",
      title: "Heavy Rain Alert",
      message: `${data.description}. Flooding possible in low-lying areas.`,
    };
  }
  // Snow (600-699)
  else if (weatherId >= 600 && weatherId < 700) {
    alert = {
      type: "info",
      icon: "snowflake",
      title: "Snow Advisory",
      message: `${data.description}. Drive carefully and expect delays.`,
    };
  }
  // Atmosphere hazards - Fog, Mist, Haze, etc. (700-799)
  else if (weatherId >= 700 && weatherId < 800) {
    if ([711, 731, 751, 761, 762].includes(weatherId)) {
      alert = {
        type: "warning",
        icon: "smog",
        title: "Air Quality Warning",
        message: `${data.description}. Limit outdoor exposure.`,
      };
    } else if (weatherId === 781) {
      alert = {
        type: "danger",
        icon: "tornado",
        title: "Tornado Warning",
        message: "Tornado detected! Seek shelter immediately!",
      };
    } else if ([701, 741].includes(weatherId)) {
      alert = {
        type: "info",
        icon: "smog",
        title: "Visibility Advisory",
        message: `${data.description}. Reduced visibility conditions.`,
      };
    }
  }
  // Extreme (800+) - clear/clouds don't need alerts
  else if (weatherId === 771) {
    alert = {
      type: "warning",
      icon: "wind",
      title: "High Wind Warning",
      message: "Squalls detected. Secure loose objects.",
    };
  }

  if (alert) {
    const alertDiv = document.createElement("div");
    alertDiv.className = `weather-alert alert-${alert.type}`;
    alertDiv.innerHTML = `
      <div class="alert-icon"><i class="fas fa-${alert.icon}"></i></div>
      <div class="alert-content">
        <strong>${alert.title}</strong>
        <p>${alert.message}</p>
      </div>
      <button class="alert-close" onclick="this.parentElement.remove()">
        <i class="fas fa-times"></i>
      </button>
    `;
    alertsContainer.appendChild(alertDiv);
  }
}
