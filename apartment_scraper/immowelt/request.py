import json

from apartment_scraper.immowelt import post_request


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
    def __init__(self, access_token: str) -> None:
        self.access_token = access_token
        self.bearer_token = f"Bearer {self.access_token}"

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
                "paging": {"size": 200, "page": 1},
            }
        )


def main():
    token_request = ImmoweltTokenRequest()
    response = post_request(token_request)
    access_token = response.json()["access_token"]

    request = ImmoweltRequest(access_token)
    response = post_request(request)
    print(response.json())


if __name__ == "__main__":
    main()
