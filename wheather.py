import requests
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import sys


sns.set(style='darkgrid')

def fetch_weather_forecast(api_key, city):
    """
    Fetch 5 day / 3 hour forecast data from OpenWeatherMap for a given city.
    """
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch data: {response.status_code} - {response.text}")
        sys.exit(1)
    return response.json()

def parse_forecast_data(forecast_json):
    """
    Parse the forecast JSON to extract datetime, temperature, and humidity.
    """
    timestamps = []
    temps = []
    humidities = []

    for entry in forecast_json.get('list', []):
        dt = datetime.fromtimestamp(entry['dt'])
        temp = entry['main']['temp']
        humidity = entry['main']['humidity']

        timestamps.append(dt)
        temps.append(temp)
        humidities.append(humidity)

    return timestamps, temps, humidities

def plot_weather_data(timestamps, temps, humidities, city):
    """
    Plot temperature and humidity over time using seaborn/matplotlib.
    """
    fig, ax1 = plt.subplots(figsize=(12,6))

    ax1.set_title(f'5 Day Weather Forecast for {city}', fontsize=16)
    ax1.set_xlabel('Date and Time')
    ax1.set_ylabel('Temperature (°C)', color='red')
    ax1.plot(timestamps, temps, 'o-', color='red', label='Temperature (°C)')
    ax1.tick_params(axis='y', labelcolor='red')
    plt.xticks(rotation=45)

    ax2 = ax1.twinx()
    ax2.set_ylabel('Humidity (%)', color='blue')
    ax2.plot(timestamps, humidities, 's-', color='blue', label='Humidity (%)')
    ax2.tick_params(axis='y', labelcolor='blue')

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("OpenWeatherMap 5 Day Forecast Visualization")

    # Instructions for the user:
    # 1. Get your free API key from https://openweathermap.org/api
    # 2. Run this script and provide your API key and city when prompted.
    # Example city input: London,UK

    api_key = input("Enter your OpenWeatherMap API key: ").strip()
    city = input("Enter the city name (e.g. London,UK): ").strip()

    if not api_key:
        print("Error: API key is required. Get it from https://openweathermap.org/api")
        sys.exit(1)

    if not city:
        print("Error: City name is required.")
        sys.exit(1)

    forecast_json = fetch_weather_forecast(api_key, city)
    timestamps, temps, humidities = parse_forecast_data(forecast_json)
    plot_weather_data(timestamps, temps, humidities, city)

