import sys
sys.path.append('.')
import json

import requests

from gpteasy import GPT
from gpteasy.gpt import GptFunction


def get_current_weather(location, unit="celsius"):
    """Get the current weather in a given location"""
    weather_info = requests.get(f'https://goweather.herokuapp.com/weather/{location}').json()
    return json.dumps(weather_info)


if __name__ == "__main__":
    gpt = GPT()
    gpt.model = 'gpt-4-0613'  # After June 27th, 2023, you can use the GPT-4 model

    # Define a function that GPT can call when it needs extra info. In this case, it's the weather
    gcw = GptFunction(name="get_current_weather", description="Get the current weather in a given location")
    gcw.add_param(name="location", type="string", description="The city", required=True)
    gcw.add_param(name="unit", type="string", enum=["celsius", "fahrenheit"])
    gcw.callback = get_current_weather  # Actual Python function to call
    gpt.add_function(gcw)

    message = gpt.chat("What's the weather like in Amsterdam?")
    print(message.text)
