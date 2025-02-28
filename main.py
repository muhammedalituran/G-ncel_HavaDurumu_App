import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry
import requests

location = input("Sehir: ").lower()

geocode_response = requests.get(f"https://geocoding-api.open-meteo.com/v1/search?name={location}&count=1&language=tr&format=json")

L1 = geocode_response.json()["results"][0]["latitude"]
L2 = geocode_response.json()["results"][0]["longitude"]


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": L1,
	"longitude": L2,
	"current": "temperature_2m",
	"timezone": "auto",
	"forecast_days": 1
}
responses = openmeteo.weather_api(url, params=params)

# Process first location. Add a for-loop for multiple locations or weather models
response = responses[0]

# Current values. The order of variables needs to be the same as requested.
current = response.Current()
current_temperature_2m = int(current.Variables(0).Value())

print(f"{location} güncel sıcaklık :{current_temperature_2m} Derece")
