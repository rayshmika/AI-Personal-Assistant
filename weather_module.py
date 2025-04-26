import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_weather(location):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        desc = data["weather"][0]["description"].capitalize()
        temp = data["main"]["temp"]
        return f"The weather in {location} is {desc} with a temperature of {temp}°C."
    else:
        return f"Sorry, I couldn't find the weather for '{location}'."
