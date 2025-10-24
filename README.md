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
