import pytest
import requests
import configparser
from dotenv import load_dotenv
import os
from enums.environment import Env

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
def env():
    """Loads the environment from the .env file and validates it."""
    if not os.path.exists('.env'):
        pytest.fail("The .env file is missing. Please create it and set the ENV variable.")
        
    load_dotenv()
    env_value = os.getenv("ENV")

    if not env_value:
        pytest.fail("The ENV variable is not set in the .env file.")

    try:
        return Env(env_value)
    except ValueError:
        valid_envs = [e.value for e in Env]
        pytest.fail(f"Invalid ENV value '{env_value}' in .env file. Must be one of: {valid_envs}")

@pytest.fixture(scope="session")
def config(env):
    """Loads the configuration from config.ini for the specified environment."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config[env.value]

@pytest.fixture(scope="session")
def secrets(env):
    """Loads secrets from secrets.ini for the specified environment."""
    secrets = configparser.ConfigParser()
    secrets.read('secrets.ini')
    return secrets[env.value]

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
