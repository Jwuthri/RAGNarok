import pytest
import requests_mock

from src.infrastructure.tools.search.brave_search import BraveSearchTool


@pytest.fixture
def brave_search_tool():
    return BraveSearchTool()


def test_brave_search_successful_response(brave_search_tool):
    with requests_mock.Mocker() as m:
        # Mock the API response
        test_query = "test"
        test_search_type = "web"
        mocked_url = brave_search_tool.base_url.format(search_type=test_search_type)
        mocked_response = {"web": {"results": [{"title": "Test Title", "url": "https://example.com"}]}}
        m.get(mocked_url, json=mocked_response)

        # Call the search method
        response = brave_search_tool.search(query=test_query, search_type=test_search_type)

        # Verify the response
        assert response == mocked_response["web"]["results"]
