import pytest
from assertpy import assert_that
from api_services.market.filters.eod_filters import EodFilters
from api_services.market.schemas.error_response_schema import ErrorResponseSchema
from utils.base_assertions import BaseAssertions


@pytest.mark.negative
@pytest.mark.parametrize("test_case_name, filters_dict, expected_error_code, expected_error_message", [
    (
            "Invalid Symbol",
            {"symbols": "INVALID_SYMBOL"},
            "no_valid_symbols_provided",
            "At least one valid symbol must be provided"
    ),
    (
            "Invalid Sort Value",
            {"symbols": "AAPL", "sort": "INVALID_SORT"},
            "validation_error",
            "the value you selected is not a valid choice"
    )
])
def test_get_eod_data_negative_scenarios(market_controller, test_case_name, filters_dict,
                                         expected_error_code, expected_error_message):
    """
    Tests the GET /eod endpoint for various invalid inputs.
    It verifies that the API returns a 422 status code and the correct error message.
    """
    filters = EodFilters(**filters_dict)
    error_schema = ErrorResponseSchema()

    response = market_controller.get_eod_data(filters)
    response_json = response.json()

    BaseAssertions.assert_status_code(response, 422)
    error_dto = BaseAssertions.validate_and_deserialize(response_json, error_schema)

    assert_that(error_dto.error.code).is_equal_to(expected_error_code)
    assert_that(error_dto.error.message).contains(expected_error_message)


@pytest.mark.negative
def test_get_eod_data_missing_symbols(api_client):
    """
    Tests that the API returns an error when the 'symbols' parameter is missing.
    This test bypasses the EodFilters dataclass to send a raw request without 'symbols'.
    """
    error_schema = ErrorResponseSchema()
    expected_error_code = "validation_error"
    expected_error_message = "You have to specify at least one symbol"

    response = api_client.get("/eod", params={})
    response_json = response.json()

    BaseAssertions.assert_status_code(response, 422)
    error_dto = BaseAssertions.validate_and_deserialize(response_json, error_schema)

    assert_that(error_dto.error.code).is_equal_to(expected_error_code)
    assert_that(error_dto.error.message).contains(expected_error_message)
