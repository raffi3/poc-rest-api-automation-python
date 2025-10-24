import pytest
from assertpy import assert_that
from api_services.market.filters.eod_filters import EodFilters
from api_services.market.schemas.eod_response_schema import EodResponseSchema
from utils.base_assertions import BaseAssertions


@pytest.mark.smoke
@pytest.mark.parametrize("symbol", ["AAPL", "MSFT", "TSLA", "NVDA"])
def test_get_eod_data_with_symbols(market_controller, symbol):
    """
    Tests the GET /eod endpoint for a single valid symbol.
    It verifies the status code, response schema, and that data is returned.
    """
    filters = EodFilters(symbols=symbol)
    expected_schema = EodResponseSchema()

    response = market_controller.get_eod_data(filters)
    response_json = response.json()

    BaseAssertions.assert_status_code(response, 200)
    eod_response_dto = BaseAssertions.validate_and_deserialize(response_json, expected_schema)

    assert_that(eod_response_dto.pagination.total).is_greater_than(0)
    assert_that(eod_response_dto.data).is_not_empty()
    assert_that(eod_response_dto.data[0].symbol).is_equal_to(symbol)


@pytest.mark.regression
@pytest.mark.parametrize("symbol, filters, expected_count", [
    ("AAPL", {"limit": 5}, 5),
    ("MSFT", {"sort": "ASC"}, 100)  # Default limit is 100
])
def test_get_eod_data_with_filters(market_controller, symbol, filters, expected_count):
    """
    Tests that optional filters like 'limit' and 'sort' work as expected.
    """
    request_filters = EodFilters(symbols=symbol, **filters)
    expected_schema = EodResponseSchema()

    response = market_controller.get_eod_data(request_filters)
    response_json = response.json()

    BaseAssertions.assert_status_code(response, 200)
    eod_response_dto = BaseAssertions.validate_and_deserialize(response_json, expected_schema)

    assert_that(eod_response_dto.data).is_length(expected_count)
