
from cmath import log
from datetime import datetime
import json
from urllib import request
from Utilities.utilities import log


# Tool 1: Get the current date and time
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Tool 2: Get the current weather for a city
def get_city_weather(city):
    url = f"https://wttr.in/{city}?format=3"
    response = request.urlopen(url, timeout=10)
    response.raise_for_status()  # Raise an error for bad responses (4xx or 5xx)
    return response.read().decode("utf-8").strip()

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

def run_tool_call(tool_call):
    func_name = tool_call.function.name
    func_args = {}
    try:
        func_args = json.loads(tool_call.function.arguments)
        log(f"tool call: {func_name} with arguments: {func_args}")
        fn = FUNCTION_NAME_TO_FUNCTION_MAPPING.get(func_name)
        result = fn(**func_args) if fn else None
    except Exception as e:
        result = f"Error executing tool '{func_name}': {str(e)}"

    log(f"    result: {result}")
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": str(result) if result is not None else "No result returned from the tool."
    }