import json


class WohnungenWien:
    def __init__(self, bearer_token: str, page: int = 0, rows: int = 500) -> None:
        self.bearer_token = bearer_token
        self._page = page
        self.rows = rows

    @property
    def url(self) -> str:
        return "https://api.immowelt.com/residentialsearch/v1/searches"

    @property
    def header(self) -> dict[str, str]:
        return {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": self.bearer_token,
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        }

    @property
    def page(self) -> int:
        return self._page

    @page.setter
    def page(self, value: int):
        self._page = value

    @property
    def body(self) -> str:
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
