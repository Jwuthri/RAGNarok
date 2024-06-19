import pytest
import requests_mock

from ragnarok.core.tools.weather.open_weather import OpenWeatherTool


@pytest.fixture
def open_weather_tool():
    return OpenWeatherTool()


def test_open_weather_search_successful_response(open_weather_tool):
    with requests_mock.Mocker() as m:
        city = "Paris"
        geo_url = open_weather_tool.city_url
        weather_url = open_weather_tool.weather_url
        # Mock the API response for city location lookup
        geo_mock_response = [{"name": "Paris", "lat": 48.8566, "lon": 2.3522}]
        # Mock the API response for weather lookup based on coordinates
        weather_mock_response = {"weather": [{"main": "Clear", "description": "clear sky"}], "main": {"temp": 289.92}}

        m.get(geo_url, json=geo_mock_response)
        m.get(weather_url, json=weather_mock_response)

        # Call the search method
        response = open_weather_tool.search(city=city)

        # Verify the response
        assert response == weather_mock_response
