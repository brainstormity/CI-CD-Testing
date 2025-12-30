import pytest
from playwright.sync_api import sync_playwright, APIRequestContext
from typing import Generator

@pytest.fixture(scope="session")
def api_request_context() -> Generator[APIRequestContext, None, None]:
    with sync_playwright() as p:
        request_context = p.request.new_context(base_url="http://127.0.0.1:8000")
        yield request_context
        request_context.dispose()

def test_root_endpoint(api_request_context: APIRequestContext):
    """Test the welcome message at the root endpoint."""
    response = api_request_context.get("/")
    assert response.ok
    assert response.json() == {"message": "Welcome to the CI/CD Learning API!"}

def test_get_items(api_request_context: APIRequestContext):
    """Test fetching all items."""
    response = api_request_context.get("/items")
    assert response.ok
    items = response.json()
    assert isinstance(items, list)
    assert len(items) >= 2
    assert items[0]["name"] == "Laptop"

def test_create_item(api_request_context: APIRequestContext):
    """Test creating a new item via POST."""
    new_item = {
        "id": 100,
        "name": "Headphones",
        "description": "Noise cancelling"
    }
    response = api_request_context.post("/items", data=new_item)
    assert response.ok
    assert response.json() == new_item

    # Verify it can be fetched
    get_response = api_request_context.get("/items/100")
    assert get_response.ok
    assert get_response.json()["name"] == "Headphones"

def test_get_invalid_item(api_request_context: APIRequestContext):
    """Test fetching a non-existent item."""
    response = api_request_context.get("/items/999")
    assert response.status == 404
    assert response.json()["detail"] == "Item not found"
