from api_services.market.filters.eod_filters import EodFilters
from api_services.market.filters.timezone_filters import TimezoneFilters

class MarketController:
    """
    Controller to interact with the 'market' related endpoints of the API.
    """

    def __init__(self, api_client):
        """
        Initializes the MarketController.

        :param api_client: Instance of APIClient for HTTP requests.
        """
        self.api_client = api_client

    def get_eod_data(self, filters: EodFilters):
        """
        Gets end-of-day data from the /eod endpoint.

        :param filters: An EodFilters object containing the query parameters.
        :return: The response object from the GET request.
        """
        endpoint = "/eod"
        return self.api_client.get(endpoint, params=filters.serialize())

    def get_timezones(self, filters: TimezoneFilters):
        """
        Gets timezone data from the /timezones endpoint.

        :param filters: TimezoneFilters object containing query params.
        :return: The response object from the GET request.
        """
        endpoint = "/timezones"
        return self.api_client.get(endpoint, params=filters.serialize())
