# API Automation Framework

This is a Python-based API test automation framework for the Marketstack API.
It uses `pytest`, `marshmallow` (for DTO handling) and `allure` (for reporting).

## Setup

1.  **Clone the repository**
2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Add your API Key:**
    -   Create the `secrets.ini` file in the project root (copy from ```secrets.ini.example```).
    -   Replace `API_ACCESS_KEY` with your actual Marketstack API access key.

5. **Install allure (command line):** 
   - MacOS/Linux: ```brew install allure```
   - Windows: ```scoop install allure```
   - Linux DEB package: ```sudo dpkg -i allure_2.29.0-1_all.deb```
   - Otherwise, refer to official documentation: https://allurereport.org/docs/install/ 

## Running Tests

### Standard Pytest Run

From the root `api_automation_framework` directory, run:

```bash
pytest
```

Run specific markers:

```bash
# Run only smoke tests
pytest -m smoke

# Run only regression tests
pytest -m regression
```

![API Tests Run](https://github.com/user-attachments/assets/692166a0-1243-4a1b-b322-e0fee022c00d)

### Allure Reporting

This framework is configured to generate Allure reports.

1.  **Run tests & Generate Allure data:**
    ```bash
    pytest --alluredir=allure-results
    ```
    (This runs all tests and saves the results to the `allure-results` folder, clearing old results first)

2.  **Serve the Allure Report:**
    Once the tests are finished, run:
    ```bash
    allure serve allure-results
    ```
    This will open the interactive Allure report in your web browser.

![Allure Report](https://github.com/user-attachments/assets/b1bd0255-cdfa-45ba-9c93-e0ae9dcf0121)


### Test Validation Strategy

| **Test / Scenario** | **Assertion/Check** | **Reason** | 
| :--- | :--- | :--- |
| **All Tests** | HTTP Status Code Validation | To confirm the server processed the request as expected (e.g., `200` for success, `422` for a known error). | 
| **All Tests** | Response Schema and Data Types Validation | To enforce the API "contract," ensuring all required fields are present, data types are correct, and no unexpected fields are returned. | 
| `test_get_eod_data_with_symbols` | `pagination.total` is greater than 0 | To confirm the API found at least one record for the symbol. | 
| `test_get_eod_data_with_symbols` | `data` list is not empty | To ensure the API is returning data records. | 
| `test_get_eod_data_with_symbols` | `data[0].symbol` matches the requested symbol | To verify the API returned data for the correct symbol that was requested. | 
| `test_get_eod_data_with_filters` | Number of items in `data` list equals `expected_count` | To verify that API filters like `limit` are being applied correctly. | 
| `test_get_eod_data_negative_scenarios` | `error.code` matches `expected_error_code` | To verify the API fails *for the correct reason* (e.g., `no_valid_symbols_provided`). | 
| `test_get_eod_data_negative_scenarios` | `error.message` contains `expected_error_message` | To ensure the API provides a helpful and correct error message to the user. | 
| `test_get_eod_data_missing_symbols` | `error.code` is `validation_error` | To verify the API correctly identifies a missing required parameter. | 
| `test_get_eod_data_missing_symbols` | `error.message` contains "You have to specify at least one symbol" | To confirm the specific error message for this missing parameter is correct. | 
| `test_get_all_timezones` | `pagination.total` is greater than 0 | To confirm the API is returning a list of timezones. | 
| `test_get_all_timezones` | `data` list contains a known value (e.g., "America/New_York") | To perform a quick "spot check" that the returned data is valid and as expected. | 
| `test_get_timezones_with_pagination` | `pagination.limit` and `pagination.offset` match request | To verify the API correctly reports the pagination parameters it used. | 
| `test_get_timezones_with_pagination` | Number of items in `data` list matches `limit` | To verify the `limit` filter is correctly applied to the data set. | 
| `test_timezone_abbreviations` | `abbr` and `abbr_dst` fields match expected values | To verify specific business logic and data points within the API response are correct. |


## Project structure
```bash
poc-rest-api-automation-python/
│
├── api_services/
│   └── market/
│       ├── filters/
│       │   ├── eod_filters.py       # Dataclass for /eod endpoint query parameters.
│       │   └── timezone_filters.py  # Dataclass for /timezones query parameters.
│       ├── schemas/
│       │   ├── common_schemas.py            # Reusable schemas (e.g., Pagination).
│       │   ├── eod_response_schema.py       # Schema & DTO for the /eod response.
│       │   ├── error_response_schema.py     # Schema & DTO for API error responses.
│       │   └── timezone_response_schema.py  # Schema & DTO for /timezones response.
│       └── market_controller.py             # Class that makes API calls (e.g., get_eod_data).
│
├── enums/
│   └── environment.py                    # Enum for environments (DEV, STAGE, PROD).
│
├── tests/
│   ├── conftest.py                       # Test-level conftest (provides 'market_controller').
│   ├── test_market_eod_negative.py       # Negative tests for the /eod endpoint.
│   ├── test_market_eod_positive.py       # Positive tests for the /eod endpoint.
│   └── test_market_timezones_positive.py # Positive tests for the /timezones endpoint.
│
├── utils/
│   ├── base_assertions.py    # Reusable assertions (assert_status_code, etc.).
│   └── dataclass_factory.py  # Helper to convert dataclasses to dicts.
│
├── .env                    # Local environment file (e.g., ENV=dev). Not in git.
├── .env.example            # Example template for the .env file.
├── .flake8                 # Configuration for code style linting.
├── config.ini              # Non-secret configs (URLs, versions) by environment.
├── conftest.py             # Root conftest (provides 'api_client' fixture).
├── pytest.ini              # Pytest configuration (markers, Allure reports).
├── README.md               # This file! Project documentation.
├── requirements.txt        # List of all Python packages needed for the project.
└── secrets.ini             # Secret API keys. Not in git.
```
