from marshmallow import ValidationError
from assertpy import assert_that
import allure

class BaseAssertions:
    """A collection of common assertion helpers for API tests."""

    @staticmethod
    @allure.step("Verify response status code is {expected_code}")
    def assert_status_code(response, expected_code):
        """
        Asserts that the response status code matches the expected code.
        """
        assert_that(response.status_code).is_equal_to(expected_code)

    @staticmethod
    @allure.step("Validate response schema and deserialize to DTO")
    def validate_and_deserialize(json_data, schema_instance):
        """
        Validates the JSON data against a Marshmallow schema and returns the deserialized DTO.
        Fails the test if validation fails.
        """
        try:
            # load() validates and deserializes in one step
            deserialized_data = schema_instance.load(json_data)
            return deserialized_data
        except ValidationError as err:
            # Fail the test with clear message showing the validation errors
            assert False, f"Schema validation failed: {err.messages}"
