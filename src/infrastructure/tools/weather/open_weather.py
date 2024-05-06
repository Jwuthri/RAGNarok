from typing import Optional
import requests

from src import API_KEYS
from src.infrastructure.tools import run_tool
from src.infrastructure.tools.tools_generator import FunctionToOpenAITool
from src.schemas.chat_message import ChatMessageSchema
from src.schemas.models import ChatOpenaiGpt35
from src.infrastructure.chat import OpenaiChat


class OpenWeatherTool:
    def __init__(self, api_key: str = API_KEYS.OPENWEATHERMAP_API_KEY, search_kwargs: Optional[dict] = None) -> None:
        self.api_key = api_key
        self.city_url = "http://api.openweathermap.org/geo/1.0/direct"
        self.weather_url = "https://api.openweathermap.org/data/2.5/weather"
        self.search_kwargs = search_kwargs if search_kwargs is not None else {}

    def search(self, city: str = "Paris") -> list[dict]:
        """
        This Python function searches for weather information based on a specified city using an API
        key.

        :param city: The `city` parameter in the `search` method is a string that represents the name of
        the city for which weather information is being searched. By default, the value is set to
        "Paris" if no city name is provided when calling the method, defaults to Paris
        :type city: str (optional)
        :return: the weather information for the specified city (default city is Paris) in the form of a
        list of dictionaries.
        """
        params = {**self.search_kwargs, **{"q": city, "limit": 5, "appid": self.api_key}}
        response = requests.get(self.city_url, params=params)
        if not response.ok:
            raise Exception(f"HTTP error {response.status_code}")

        infos = response.json()
        if len(infos):
            lat, lon = infos[0]["lat"], infos[0]["lon"]
            params = {**self.search_kwargs, **{"lat": lat, "lon": lon, "appid": self.api_key}}
            response = requests.get(self.weather_url, params=params)
            if not response.ok:
                raise Exception(f"HTTP error {response.status_code}")
            return response.json()

        return []


def weather_tool(city: str) -> list[dict]:
    """
    The function `query_weather` takes a city name as input and returns a list of dictionaries
    containing weather information for that city using the OpenWeatherTool.

    :param city: The `city` parameter in the `query_weather` function is a string that represents the
    name of the city for which you want to query the weather information
    :type city: str
    :return: A list of dictionaries containing weather information for the specified city.
    """
    return OpenWeatherTool().search(city=city)


if __name__ == "__main__":
    tool_transformer = FunctionToOpenAITool(weather_tool).generate_tool_json()
    print(tool_transformer)
    messages = [
        ChatMessageSchema(role="system", message="You are an ai assistant, Use tools when you can"),
        ChatMessageSchema(role="user", message="what is the weather in paris?"),
    ]
    res = OpenaiChat(ChatOpenaiGpt35()).predict(messages, tools=[tool_transformer])
    print(res)
    func_res = run_tool(res.tool_call, {"weather_tool": weather_tool})
    print(func_res)
    messages = [
        ChatMessageSchema(role="system", message="You are an ai assistant, Use tools when you can"),
        ChatMessageSchema(role="user", message="do you like flowers?"),
    ]
    res = OpenaiChat(ChatOpenaiGpt35()).predict(messages, tools=[tool_transformer])
    print(res)
    func_res = run_tool(res.tool_call, {"weather_tool": weather_tool})
    print(func_res)
