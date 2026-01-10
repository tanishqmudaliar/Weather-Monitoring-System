// javascript
    // Global variables
    let currentUnit = "metric"; // 'metric' or 'imperial'
    let lastLocation = ""; // Store the last searched location
    let forecastChart = null;

    // DOM Elements
    const locationInput = document.getElementById("location-input");
    const searchBtn = document.getElementById("search-btn");
    const geolocationBtn = document.getElementById("geolocation-btn");
    const metricToggle = document.getElementById("metric-toggle");
    const imperialToggle = document.getElementById("imperial-toggle");
    const tabButtons = document.querySelectorAll(".tab-btn");
    const tabPanes = document.querySelectorAll(".tab-pane");

    // Event Listeners
    document.addEventListener("DOMContentLoaded", setupEventListeners);

    function setupEventListeners() {
      if (searchBtn) searchBtn.addEventListener("click", handleSearch);
      if (locationInput) {
        locationInput.addEventListener("keypress", (e) => {
          if (e.key === "Enter") handleSearch();
        });
      }
      if (geolocationBtn) geolocationBtn.addEventListener("click", getUserLocation);
      if (metricToggle) metricToggle.addEventListener("click", () => changeUnit("metric"));
      if (imperialToggle) imperialToggle.addEventListener("click", () => changeUnit("imperial"));

      tabButtons.forEach((button) => {
        button.addEventListener("click", () => switchTab(button.dataset.tab));
      });

      // Add quick city tag listeners
      const quickCityTags = document.querySelectorAll(".quick-city-tag");
      quickCityTags.forEach((tag) => {
        tag.addEventListener("click", () => {
          const city = tag.getAttribute("data-city");
          if (city && locationInput) {
            locationInput.value = city;
            handleSearch();
          }
        });
      });
    }

    // Tab Switching
    function switchTab(tabId) {
      // Update active tab button
      tabButtons.forEach((btn) => {
        btn.classList.toggle("active", btn.dataset.tab === tabId);
      });

      // Update active tab pane
      tabPanes.forEach((pane) => {
        pane.classList.toggle("active", pane.id === tabId);
      });

      // Load data for the selected tab if needed
      if (lastLocation) {
        const currentWeatherEl = document.getElementById("current-weather");
        if (tabId === "current" && currentWeatherEl && currentWeatherEl.classList.contains("hidden")) {
          fetchCurrentWeather(lastLocation);
        } else if (tabId === "forecast") {
          const cards = document.getElementById("forecast-cards");
          if (cards && cards.children.length === 0) {
            fetchForecastData(lastLocation);
          }
        }
      }
    }

    // Handle search
    function handleSearch() {
      const location = locationInput.value.trim();
      if (location) {
        lastLocation = location;
        fetchCurrentWeather(location);

        // If forecast tab is active, fetch forecast data
        const forecastTab = document.getElementById("forecast");
        if (forecastTab && forecastTab.classList.contains("active")) {
          fetchForecastData(location);
        }
      }
    }

    // Geolocation -> now uses server-side proxy to avoid exposing API key
    function getUserLocation() {
      if (!navigator.geolocation) {
        alert("Geolocation is not supported by your browser");
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

          // Call backend endpoint that uses the API key from the server environment
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
                fetchCurrentWeather(city);

                const forecastTab = document.getElementById("forecast");
                if (forecastTab && forecastTab.classList.contains("active")) {
                  fetchForecastData(city);
                }
              } else {
                showError("current");
              }
            })
            .catch((error) => {
              console.error("Error in reverse geocoding:", error);
              showError("current");
            })
            .finally(() => {
              if (geolocationBtn) {
                geolocationBtn.disabled = false;
                geolocationBtn.innerHTML = '<i class="fas fa-map-marker-alt"></i>';
              }
            });
        },
        (error) => {
          console.error("Geolocation error:", error);
          if (geolocationBtn) {
            geolocationBtn.disabled = false;
            geolocationBtn.innerHTML = '<i class="fas fa-map-marker-alt"></i>';
          }
          showError("current");
        }
      );
    }

    // Unit conversion
    function changeUnit(unit) {
      if (currentUnit === unit) return;

      currentUnit = unit;
      if (metricToggle) metricToggle.classList.toggle("active", unit === "metric");
      if (imperialToggle) imperialToggle.classList.toggle("active", unit === "imperial");

      // Update displayed temperature values
      updateTemperatureDisplays();

      // If we have last location data, refresh the current weather display
      const currentTab = document.getElementById("current");
      if (lastLocation && currentTab && currentTab.classList.contains("active")) {
        fetchCurrentWeather(lastLocation);
      }

      // Reload forecast chart if it exists and we have a location
      const forecastTab = document.getElementById("forecast");
      if (forecastChart && forecastTab && forecastTab.classList.contains("active") && lastLocation) {
        fetchForecastData(lastLocation);
      }
    }

    function updateTemperatureDisplays() {
      const tempElements = document.querySelectorAll(".temp-value");
      const tempUnitElements = document.querySelectorAll(".temp-unit");

      // Update unit display
      tempUnitElements.forEach((el) => {
        el.textContent = currentUnit === "metric" ? "°C" : "°F";
      });

      // Update temperature values if we have data-temp-c and data-temp-f attributes
      tempElements.forEach((el) => {
        if (el.hasAttribute("data-temp-c") && el.hasAttribute("data-temp-f")) {
          const tempC = parseFloat(el.getAttribute("data-temp-c"));
          const tempF = parseFloat(el.getAttribute("data-temp-f"));
          if (!isNaN(tempC) && !isNaN(tempF)) {
            el.textContent = currentUnit === "metric" ? tempC.toFixed(1) : tempF.toFixed(1);
          }
        }
      });
    }

    // Fetch Current Weather
    function fetchCurrentWeather(location) {
      const loader = document.getElementById("weather-loader");
      const weatherPane = document.getElementById("current-weather");
      const errorPane = document.getElementById("weather-error");

      if (loader) loader.classList.remove("hidden");
      if (weatherPane) weatherPane.classList.add("hidden");
      if (errorPane) errorPane.classList.add("hidden");

      fetch(`/api/current-weather?location=${encodeURIComponent(location)}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error("Network response was not ok");
          }
          return response.json();
        })
        .then((data) => {
          displayCurrentWeather(data);
        })
        .catch((error) => {
          console.error("Error fetching current weather:", error);
          showError("current");
        })
        .finally(() => {
          if (loader) loader.classList.add("hidden");
        });
    }

    function displayCurrentWeather(data) {
      if (!data) return;

      const locationNameEl = document.getElementById("location-name");
      if (locationNameEl) {
        const locationText = locationNameEl.querySelector("span");
        if (locationText) locationText.textContent = data.location || "";
      }

      const timeEl = document.getElementById("current-time");
      if (timeEl) {
        const timeText = timeEl.querySelector("span");
        if (timeText) timeText.textContent = new Date().toLocaleString();
      }

      const weatherIcon = document.getElementById("weather-icon");
      if (weatherIcon && data.icon) {
        weatherIcon.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
        weatherIcon.alt = data.description || "";
      }

      // Temperatures
      const tempC = Number(data.temperature) || 0;
      const tempF = (tempC * 9) / 5 + 32;
      const currentTemp = document.getElementById("current-temp");
      if (currentTemp) {
        currentTemp.textContent = currentUnit === "metric" ? tempC.toFixed(1) : tempF.toFixed(1);
        currentTemp.setAttribute("data-temp-c", tempC);
        currentTemp.setAttribute("data-temp-f", tempF);
      }

      const descEl = document.getElementById("weather-description");
      if (descEl) {
        const descText = descEl.querySelector("span");
        if (descText) descText.textContent = data.description || "";
      }

      // Feels like
      const feelsLikeC = Number(data.feels_like) || 0;
      const feelsLikeF = (feelsLikeC * 9) / 5 + 32;
      const feelsLike = document.getElementById("feels-like");
      if (feelsLike) {
        feelsLike.textContent = currentUnit === "metric" ? feelsLikeC.toFixed(1) : feelsLikeF.toFixed(1);
        feelsLike.setAttribute("data-temp-c", feelsLikeC);
        feelsLike.setAttribute("data-temp-f", feelsLikeF);
      }

      const humidityEl = document.getElementById("humidity");
      if (humidityEl) humidityEl.textContent = `${data.humidity || 0}%`;

      const pressureEl = document.getElementById("pressure");
      if (pressureEl) pressureEl.textContent = `${data.pressure || 0} hPa`;

      const windSpeedElement = document.getElementById("wind-speed");
      const windSpeedMps = Number(data.wind_speed) || 0;
      const windSpeedMph = windSpeedMps * 2.237;
      if (windSpeedElement) {
        windSpeedElement.textContent = currentUnit === "metric" ? `${windSpeedMps.toFixed(1)} m/s` : `${windSpeedMph.toFixed(1)} mph`;
      }

      // Sunrise / Sunset
      if (data.sunrise && data.sunset) {
        const sunriseDate = new Date(data.sunrise * 1000);
        const sunsetDate = new Date(data.sunset * 1000);
        const sunriseEl = document.getElementById("sunrise");
        const sunsetEl = document.getElementById("sunset");
        if (sunriseEl) sunriseEl.textContent = sunriseDate.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
        if (sunsetEl) sunsetEl.textContent = sunsetDate.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
      }

      // Additional info - Wind Direction
      const windDirectionEl = document.getElementById("wind-direction");
      if (windDirectionEl && data.wind_direction !== undefined) {
        windDirectionEl.textContent = `${data.wind_direction}°`;
      }

      // Clouds
      const cloudsEl = document.getElementById("clouds");
      if (cloudsEl && data.clouds !== undefined) {
        cloudsEl.textContent = `${data.clouds}%`;
      }

      // Visibility
      const visibilityEl = document.getElementById("visibility");
      if (visibilityEl && data.visibility !== undefined) {
        const visibilityKm = (data.visibility / 1000).toFixed(1);
        visibilityEl.textContent = `${visibilityKm} km`;
      }

      const weatherPane = document.getElementById("current-weather");
      if (weatherPane) weatherPane.classList.remove("hidden");
    }

    // Fetch Forecast Data
    function fetchForecastData(location) {
      if (!location) return;

      const loader = document.getElementById("forecast-loader");
      const errorPane = document.getElementById("forecast-error");
      const cards = document.getElementById("forecast-cards");

      if (loader) loader.classList.remove("hidden");
      if (errorPane) errorPane.classList.add("hidden");
      if (cards) cards.innerHTML = "";

      fetch(`/api/forecast?location=${encodeURIComponent(location)}`)
        .then((response) => {
          if (!response.ok) throw new Error("Network response was not ok");
          return response.json();
        })
        .then((data) => {
          displayForecastData(data || []);
        })
        .catch((error) => {
          console.error("Error fetching forecast data:", error);
          showError("forecast");
        })
        .finally(() => {
          if (loader) loader.classList.add("hidden");
        });
    }

    function displayForecastData(data) {
      // Process data for chart
      const labels = [];
      const tempData = [];
      const tempMinData = [];
      const tempMaxData = [];

      // Group by date for daily forecast cards
      const dailyData = {};

      (data || []).forEach((item) => {
        const date = new Date(item.dt * 1000);
        const dateStr = date.toLocaleDateString();
        const timeStr = date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
        labels.push(timeStr);

        // Convert temperature if needed
        const temp = currentUnit === "metric" ? item.temp : (item.temp * 9) / 5 + 32;
        const tempMin = currentUnit === "metric" ? item.temp_min : (item.temp_min * 9) / 5 + 32;
        const tempMax = currentUnit === "metric" ? item.temp_max : (item.temp_max * 9) / 5 + 32;

        tempData.push(temp);
        tempMinData.push(tempMin);
        tempMaxData.push(tempMax);

        if (!dailyData[dateStr]) {
          dailyData[dateStr] = { date: date, icon: item.icon, description: item.description, temps: [], humidity: [] };
        }

        dailyData[dateStr].temps.push(temp);
        dailyData[dateStr].humidity.push(item.humidity);
      });

      createForecastChart(labels, tempData, tempMinData, tempMaxData);
      createForecastCards(dailyData);
    }

    function createForecastChart(labels, tempData, tempMinData, tempMaxData) {
      if (forecastChart && typeof forecastChart.destroy === "function") {
        forecastChart.destroy();
        forecastChart = null;
      }

      const canvas = document.getElementById("forecast-chart");
      if (!canvas) return;
      const ctx = canvas.getContext("2d");
      if (!ctx) return;

      forecastChart = new Chart(ctx, {
        type: "line",
        data: {
          labels: labels,
          datasets: [
            {
              label: `Temperature (${currentUnit === "metric" ? "°C" : "°F"})`,
              data: tempData,
              borderColor: "#e67e22",
              backgroundColor: "rgba(230, 126, 34, 0.1)",
              borderWidth: 2,
              tension: 0.3,
              fill: false,
            },
            {
              label: `Min Temperature (${currentUnit === "metric" ? "°C" : "°F"})`,
              data: tempMinData,
              borderColor: "#3498db",
              borderWidth: 1,
              borderDash: [5, 5],
              pointRadius: 0,
              fill: false,
            },
            {
              label: `Max Temperature (${currentUnit === "metric" ? "°C" : "°F"})`,
              data: tempMaxData,
              borderColor: "#e74c3c",
              borderWidth: 1,
              borderDash: [5, 5],
              pointRadius: 0,
              fill: false,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              title: { display: true, text: "Time" },
            },
            y: {
              title: { display: true, text: `Temperature (${currentUnit === "metric" ? "°C" : "°F"})` },
            },
          },
        },
      });
    }

    function createForecastCards(dailyData) {
      const forecastCardsContainer = document.getElementById("forecast-cards");
      if (!forecastCardsContainer) return;
      forecastCardsContainer.innerHTML = "";

      Object.keys(dailyData).forEach((dateStr) => {
        const day = dailyData[dateStr];

        const avgTemp = day.temps.reduce((sum, t) => sum + t, 0) / day.temps.length;
        const avgHumidity = day.humidity.reduce((sum, h) => sum + h, 0) / day.humidity.length;

        const card = document.createElement("div");
        card.className = "forecast-card";

        const date = document.createElement("div");
        date.className = "forecast-date";
        date.textContent = day.date.toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" });

        const icon = document.createElement("img");
        if (day.icon) {
          icon.src = `https://openweathermap.org/img/wn/${day.icon}@2x.png`;
          icon.alt = day.description || "";
        }

        const description = document.createElement("div");
        description.className = "forecast-description";
        description.textContent = day.description || "";

        const temp = document.createElement("div");
        temp.className = "forecast-temp";
        temp.textContent = `${avgTemp.toFixed(1)}${currentUnit === "metric" ? "°C" : "°F"}`;

        const humidity = document.createElement("div");
        humidity.className = "forecast-humidity";
        humidity.textContent = `Humidity: ${avgHumidity.toFixed(0)}%`;

        card.appendChild(date);
        card.appendChild(icon);
        card.appendChild(description);
        card.appendChild(temp);
        card.appendChild(humidity);

        forecastCardsContainer.appendChild(card);
      });
    }

    // Show error message
    function showError(section) {
      const errorElement = document.getElementById(`${section}-error`);
      if (errorElement) {
        errorElement.classList.remove("hidden");
      }
    }