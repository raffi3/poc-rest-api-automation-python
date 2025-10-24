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
