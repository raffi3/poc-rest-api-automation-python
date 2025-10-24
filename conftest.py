import pytest
import requests
import configparser
import os
from pathlib import Path
from enums.environment import Env
from dotenv import load_dotenv


class APIClient:
    """Responsible for making requests to the API, handling URL construction."""

    def __init__(self, base_url, api_version, access_key):
        """
        Initializes the APIClient.

        :param base_url: The base URL for the API (e.g., https://api.marketstack.com).
        :param api_version: The version of the API to use (e.g., /v1/).
        :param access_key: The API access key for authentication.
        """
        self.base_url = base_url
        self.api_version = api_version
        self.access_key = access_key

    def get(self, endpoint, params=None):
        """
        Makes a GET request. The access_key is added automatically.

        :param endpoint: The API endpoint (e.g., /eod).
        :param params: A dictionary of query parameters.
        :return: The response object from requests.
        """
        if params is None:
            params = {}

        # Automatically add the access key to every request
        params['access_key'] = self.access_key

        url = f"{self.base_url}{self.api_version}{endpoint}"
        print("Request URL:", url)
        return requests.get(url, params=params)


@pytest.fixture(scope="session")
def project_root(pytestconfig) -> Path:
    """Provides the absolute path to the project root directory."""
    return pytestconfig.rootpath


@pytest.fixture(scope="session")
def env(project_root):
    """Loads the environment from the .env file and validates it."""
    env_path = project_root / ".env"
    print(f"Looking for .env file at: {env_path}")

    if not env_path.exists():
        pytest.fail(f"The .env file is missing at: {env_path}. Please create it and set the ENV variable.")

    load_dotenv(dotenv_path=env_path)
    env_value = os.getenv("ENV")

    if not env_value:
        pytest.fail("The ENV variable is not set in the .env file.")

    try:
        return Env(env_value)
    except ValueError:
        valid_envs = [e.value for e in Env]
        pytest.fail(f"Invalid ENV value '{env_value}' in .env file. Must be one of: {valid_envs}")


@pytest.fixture(scope="session")
def config(env, project_root):
    """Loads the configuration from config.ini for the specified environment."""
    config = configparser.ConfigParser()
    config_path = project_root / 'config.ini'
    config.read(config_path)

    return config[env.value]


@pytest.fixture(scope="session")
def secrets(env, project_root):
    """Loads secrets from secrets.ini for the specified environment."""
    secrets = configparser.ConfigParser()
    secrets_path = project_root / 'secrets.ini'
    read_files = secrets.read(secrets_path)

    if not read_files:
        pytest.fail(
            f"Could not find or read secrets.ini at: {secrets_path}.\n"
            f"Please create it or copy from secrets.ini.example file and set variables (i.e. API_ACCESS_KEY).")
    env_name = env.value
    if env_name not in secrets:
        pytest.fail(
            f"\n\n[VALIDATION ERROR]\nThe section [{env.value}] is MISSING from your secrets.ini file."
            f"\nPlease add this section.\n"
        )

    env_object = secrets[env_name]
    # Check if the key is missing entirely
    if 'access_key' not in env_object:
        pytest.fail(
            f"\n\n[VALIDATION ERROR]"
            f"\nThe 'access_key' property is MISSING from the [{env_name}] section in your secrets.ini file."
            f"\nPlease add it: `access_key = YOUR_KEY`\n")
    access_key_val = env_object['access_key']

    # Check if the value is empty
    if not access_key_val:
        pytest.fail(
            f"\n\n[VALIDATION ERROR] The 'access_key' property in the [{env_name}] section of secrets.ini is EMPTY."
            f"\nPlease provide your API key.\n")

    # Check if it's still the placeholder value from your example
    if access_key_val == 'API_ACCESS_KEY':
        pytest.fail(f"\n\n[VALIDATION ERROR] The 'access_key' in the [{env_name}] section of secrets.ini "
                    f"is still set to the placeholder 'API_ACCESS_KEY'.\nPlease replace it with your real API key.\n")

    return env_object


@pytest.fixture(scope="session")
def base_url(config):
    """Provides the base_url from the config."""
    return config['base_url']


@pytest.fixture(scope="session")
def api_version(config):
    """Provides the api_version from the config."""
    return config['api_version']


@pytest.fixture(scope="session")
def access_key(secrets):
    """Provides the access_key from the secrets."""
    return secrets['access_key']


@pytest.fixture(scope="session")
def api_client(base_url, api_version, access_key):
    """Provides an instance of the APIClient, configured for the target environment."""
    return APIClient(base_url, api_version, access_key)
