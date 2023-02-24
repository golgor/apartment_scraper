import json
from datetime import datetime

from apartment_scraper import pkg_path
from apartment_scraper.immowelt import get_data, get_immowelt_token


class ImmoweltTokenRequest:
    @property
    def url(self) -> str:
        return "https://api.immowelt.com/auth/oauth/token"

    @property
    def header(self) -> dict[str, str]:
        return {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/x-www-form-urlencoded",
            "authorization": "Basic cmVzaWRlbnRpYWwtc2VhcmNoLXVpOlU4KzhzYn4oO1E0YlsyUXcjaHl3TSlDcTc=",
        }

    @property
    def body(self) -> dict[str, str | int]:
        return {"grant_type": "client_credentials"}


class ImmoweltRequest:
    def __init__(
        self, bearer_token: str, page: int = 0, rows: int = 500
    ) -> None:
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


def main():
    access_token = get_immowelt_token()
    request = ImmoweltRequest(access_token)

    test = get_data(request)

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"immowelt_{today}.json"

    filepath = pkg_path.joinpath("immowelt", "raw_data", filename)
    with open(filepath, "w") as f:
        f.write(json.dumps(test, indent=2))
        print(f"Successfully saved {len(test)}")


if __name__ == "__main__":
    main()
