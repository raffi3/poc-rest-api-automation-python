import pytest
from api_services.market.market_controller import MarketController

@pytest.fixture(scope="module")
def market_controller(api_client):
    """Provides a MarketController instance for the tests."""
    return MarketController(api_client)
