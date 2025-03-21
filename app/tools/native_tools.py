import datetime
import random
import requests
from typing import Dict, Any, List, Optional

def get_current_time() -> Dict[str, str]:
    """Get the current date and time"""
    now = datetime.datetime.now()
    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "timezone": datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
    }

def calculate(operation: str, x: float, y: float) -> Dict[str, Any]:
    """Perform a basic calculation operation"""
    operations = {
        "add": lambda a, b: a + b,
        "subtract": lambda a, b: a - b,
        "multiply": lambda a, b: a * b,
        "divide": lambda a, b: a / b if b != 0 else "Error: Division by zero"
    }
    
    if operation not in operations:
        return {"error": f"Unsupported operation: {operation}"}
    
    result = operations[operation](x, y)
    return {"result": result}

def random_number(min_value: int = 1, max_value: int = 100) -> Dict[str, int]:
    """Generate a random number within a range"""
    return {"number": random.randint(min_value, max_value)}

def weather_info(city: str) -> Dict[str, Any]:
    """Get mock weather information for a city"""
    weather_conditions = ["Sunny", "Cloudy", "Rainy", "Snowy", "Windy", "Foggy"]
    temperature = random.randint(-10, 40)
    humidity = random.randint(30, 90)
    
    return {
        "city": city,
        "temperature": temperature,
        "humidity": f"{humidity}%",
        "condition": random.choice(weather_conditions)
    }

def search_text(text: str, query: str) -> Dict[str, Any]:
    """Search for a query in a text"""
    if query in text:
        return {
            "found": True,
            "position": text.find(query),
            "count": text.count(query)
        }
    else:
        return {
            "found": False,
            "position": -1,
            "count": 0
        }

def real_weather(city: str, country_code: str = None) -> Dict[str, Any]:
    """Get real weather data for a location using Open-Meteo API"""
    try:
        # First, geocode the city to get coordinates
        geocode_url = "https://geocoding-api.open-meteo.com/v1/search"
        geocode_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        }
        
        if country_code:
            geocode_params["country_code"] = country_code
            
        geocode_response = requests.get(geocode_url, params=geocode_params)
        geocode_response.raise_for_status()
        geocode_data = geocode_response.json()
        
        if not geocode_data.get("results"):
            return {"error": f"Could not find location: {city}"}
        
        # Get the first result
        location = geocode_data["results"][0]
        lat = location["latitude"]
        lon = location["longitude"]
        location_name = location["name"]
        country = location.get("country", "Unknown")
        
        # Call Open-Meteo API (free, no API key required)
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,wind_speed_10m,wind_direction_10m,weather_code",
            "hourly": "temperature_2m,relative_humidity_2m",
            "timezone": "auto"
        }
        
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        
        # Map weather codes to conditions
        weather_codes = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            56: "Light freezing drizzle",
            57: "Dense freezing drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Light freezing rain",
            67: "Heavy freezing rain",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            85: "Slight snow showers",
            86: "Heavy snow showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        
        current = weather_data["current"]
        weather_code = current.get("weather_code", 0)
        weather_description = weather_codes.get(weather_code, "Unknown")
        
        # Extract relevant weather information
        return {
            "city": location_name,
            "country": country,
            "coordinates": {
                "latitude": lat,
                "longitude": lon
            },
            "temperature": {
                "current": current["temperature_2m"],
                "apparent": current["apparent_temperature"],
                "unit": weather_data["current_units"]["temperature_2m"]
            },
            "humidity": {
                "value": current["relative_humidity_2m"],
                "unit": weather_data["current_units"]["relative_humidity_2m"]
            },
            "precipitation": {
                "value": current["precipitation"],
                "unit": weather_data["current_units"]["precipitation"]
            },
            "wind": {
                "speed": current["wind_speed_10m"],
                "speed_unit": weather_data["current_units"]["wind_speed_10m"],
                "direction": current["wind_direction_10m"],
                "direction_unit": weather_data["current_units"]["wind_direction_10m"]
            },
            "weather": {
                "code": weather_code,
                "description": weather_description
            },
            "timestamp": current["time"]
        }
    except requests.exceptions.RequestException as e:
        return {"error": f"API request error: {str(e)}"}
    except (KeyError, IndexError, ValueError) as e:
        return {"error": f"Failed to parse weather data: {str(e)}"} 