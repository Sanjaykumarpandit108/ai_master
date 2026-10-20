
from datetime import datetime
from urllib import request, parse


# Tool 1: Get the current date and time
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Tool 2: Get the current weather for a city
def get_city_weather(city):
    city = parse.quote(city)
    url = f"https://wttr.in/{city}?format=3"

    with request.urlopen(url, timeout=10) as response:
        return response.read().decode("utf-8")

def get_user_city():
    # This function can be implemented to get the user's city, for example, by using geolocation or user input.
    # For now, we'll return a placeholder value.
    # take a user value from input and return it
    city = input("Please enter your city: ")
    return city

# Tool definitions for the LLM
Tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": (
                "Get the current date and time in the format "
                "YYYY-MM-DD HH:MM:SS"
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_city_weather",
            "description": "Get the current weather for a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The name of the city."
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_city",
            "description": "Get the user's city.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


# Map function names to Python functions
FUNCTION_NAME_TO_FUNCTION_MAPPING = {
    "get_current_time": get_current_time,
    "get_city_weather": get_city_weather,
    "get_user_city": get_user_city
}
