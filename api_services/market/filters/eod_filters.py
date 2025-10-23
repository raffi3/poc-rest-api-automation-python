from dataclasses import dataclass, asdict
from utils.dataclass_factory import as_dict_remove_none


@dataclass
class EodFilters:
    """
    A data class to hold the required and optional filter parameters
    for the Marketstack EOD API endpoint.
    """
    # Required parameters
    symbols: str

    # Optional parameters (default is None)
    limit: int | None = None
    offset: int | None = None
    sort: str | None = None

    def serialize(self) -> dict:
        """
        Serializes the dataclass into a dictionary, removing any fields that are None.
        The dictionary to be used as API query parameters.
        """
        return asdict(self, dict_factory=as_dict_remove_none)
