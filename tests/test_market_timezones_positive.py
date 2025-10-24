import pytest
import allure
from assertpy import assert_that, soft_assertions
from api_services.market.filters.timezone_filters import TimezoneFilters
from api_services.market.schemas.timezone_response_schema import TimezonesResponseSchema
from utils.base_assertions import BaseAssertions


@allure.feature("Market API")
@allure.story("Timezones Endpoint - Positive Scenarios")
class TestMarketTimezonesPositive:
    """
    Contains all positive test cases for the /timezones endpoint.
    """

    @allure.title("Test GET /timezones endpoint (all timezones)")
    @allure.description("Tests the GET /timezones endpoint without any optional filters.")
    @pytest.mark.smoke
    def test_get_all_timezones(self, market_controller):
        """
        Tests the GET /timezones endpoint without any optional filters.
        """
        with allure.step("Set up filters and expected schema"):
            filters = TimezoneFilters()
            expected_schema = TimezonesResponseSchema()

        with allure.step("Send GET request to /timezones"):
            response = market_controller.get_timezones(filters)
            response_json = response.json()

        with allure.step("Validate status code 200 and deserialize response"):
            BaseAssertions.assert_status_code(response, 200)
            timezones_dto = BaseAssertions.validate_and_deserialize(response_json, expected_schema)

        with allure.step("Assert response data content"):
            assert_that(timezones_dto.pagination.total).is_greater_than(0)
            assert_that(timezones_dto.data).is_not_empty()
            assert_that([tz.timezone for tz in timezones_dto.data]).contains("America/New_York")

    @allure.title("Test GET /timezones with pagination: limit={limit}, offset={offset}")
    @allure.description("Tests that pagination filters (limit, offset) work as expected for /timezones.")
    @pytest.mark.regression
    @pytest.mark.parametrize("limit, offset", [
        (5, 0),
        (10, 5)
    ])
    def test_get_timezones_with_pagination(self, market_controller, limit, offset):
        """
        Tests that pagination filters (limit, offset) work as expected for /timezones.
        """
        with allure.step(f"Set up filters: limit={limit}, offset={offset}"):
            filters = TimezoneFilters(limit=limit, offset=offset)
            expected_schema = TimezonesResponseSchema()

        with allure.step("Send GET request to /timezones"):
            response = market_controller.get_timezones(filters)
            response_json = response.json()

        with allure.step("Validate status code 200 and deserialize response"):
            BaseAssertions.assert_status_code(response, 200)
            timezones_dto = BaseAssertions.validate_and_deserialize(response_json, expected_schema)

        with allure.step("Assert pagination fields and data length"):
            assert_that(timezones_dto.pagination.limit).is_equal_to(limit)
            assert_that(timezones_dto.pagination.offset).is_equal_to(offset)
            assert_that(timezones_dto.data).is_length(limit)

    @allure.title("Test timezone abbreviations for: {timezone_name}")
    @allure.description("Tests that specific timezones have the correct abbreviation values.")
    @pytest.mark.regression
    @pytest.mark.parametrize("timezone_name, expected_abbr, expected_abbr_dst", [
        ("America/New_York", "EST", "EDT"),
        ("Europe/London", "GMT", "BST"),
        ("Asia/Tokyo", "JST", "JST"),
        ("Australia/Sydney", "AEST", "AEDT")
    ])
    def test_timezone_abbreviations(self, market_controller, timezone_name, expected_abbr, expected_abbr_dst):
        """
        Tests that specific timezones have the correct abbreviation values.
        """
        with allure.step("Set up filters and expected schema"):
            filters = TimezoneFilters()
            expected_schema = TimezonesResponseSchema()

        with allure.step("Send GET request to /timezones to fetch all data"):
            response = market_controller.get_timezones(filters)
            response_json = response.json()

        with allure.step("Validate status code 200 and deserialize response"):
            BaseAssertions.assert_status_code(response, 200)
            timezones_dto = BaseAssertions.validate_and_deserialize(response_json, expected_schema)

        with allure.step(f"Find timezone {timezone_name} and assert abbreviations"):
            # For easier check, convert the list of DTOs to a dictionary
            timezones_map = {tz.timezone: tz for tz in timezones_dto.data}

            assert_that(timezones_map).contains_key(timezone_name)

            found_timezone = timezones_map[timezone_name]
            with soft_assertions():
                assert_that(found_timezone.abbr).is_equal_to(expected_abbr)
                assert_that(found_timezone.abbr_dst).is_equal_to(expected_abbr_dst)