import json
from typing import Self


class WohnungenWien:
    """Apartments class."""
    def __init__(self: Self, bearer_token: str, page: int = 0, rows: int = 500) -> None:
        """Initialize class."""
        self.bearer_token = bearer_token
        self._page = page
        self.rows = rows

    @property
    def url(self: Self) -> str:
        """The url to fetch the apartments from."""
        return "https://api.immowelt.com/residentialsearch/v1/searches"

    @property
    def header(self: Self) -> dict[str, str]:
        """The header to use in the request."""
        return {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": self.bearer_token,
            "user-agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, "
                "like Gecko) Chrome/108.0.0.0 Safari/537.36"
            ),
        }

    @property
    def page(self: Self) -> int:
        """The page to fetch."""
        return self._page

    @page.setter
    def page(self: Self, value: int) -> None:
        self._page = value

    @property
    def body(self: Self) -> str:
        """The body of the request."""
        return json.dumps(
            {
                "estateType": "APARTMENT",
                "distributionTypes": ["SALE"],
                "estateSubtypes": [],
                "locationIds": [514061],
                "featureFilters": [],
                "excludedFeatureFilters": [],
                "primaryPrice": {"min": None, "max": None},
                "primaryArea": {"min": None, "max": None},
                "areas": [{"areaType": "PLOT_AREA", "min": None, "max": None}],
                "rooms": {"min": None, "max": None},
                "constructionYear": {"min": None, "max": None},
                "geoRadius": {
                    "radius": None,
                    "point": {
                        "lat": 48.22029015850006,
                        "lon": 16.371278701731626,
                    },
                },
                "zipCode": None,
                "sort": {"direction": "DESC", "field": "RELEVANCE"},
                "immoItemTypes": ["ESTATE", "PROJECT"],
                "paging": {"size": self.rows, "page": self.page},
            }
        )
