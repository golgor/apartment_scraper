import json
from dataclasses import dataclass, field
from typing import Any, Protocol

import requests

BEARER_TOKEN = """Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjAwMzIwMjAwNjExIn0.eyJzY29wZSI6WyJzZXJ2aWNlcyJdLCJpc3MiOiJJV1QiLCJleHAiOjE2NzY5Nzk1MjEsImNyZWF0aW9uX29mZnNldF9kYXRlX3RpbWUiOiIyMDIzLTAyLTIxVDExOjM4OjQxLjU3MTQ3NTY0OCswMTowMCIsImlhdCI6MTY3Njk3NTkyMSwiYXV0aG9yaXRpZXMiOlsicHVibGljIiwicmVjb21tZW5kZXIiLCJjbGlja3N0cmVhbWVyIl0sImp0aSI6ImdwVHgtZm0tWm1raklRaGdDSkM3dnI5MHdRYyIsInRlbmFudCI6ImltbW93ZWx0IiwiY2xpZW50X2lkIjoicmVzaWRlbnRpYWwtc2VhcmNoLXVpIn0.dOxy0H6b1hfrQi7LJtnU6A6VLaH4swZCN-Iah-a5ZsZQRNtxYXMXfqfeQo136sDaP9yv-mqqp3xM_gaWA6qN90l0BcPfTUIHWfQG5p6YaCVsEjgVZe2RMrQUsR3rcNDAmZvCPy_Gyy5mFa2ju2n4xOK6T6UAaAPGUrB-_QcdYkN9kfTI154TbB6TGjD000aA9ZsmG1fnOaC1WuDUYPQVB8PQVY1pquNZi7kyN-7K5csgJ4xxALEs6_MQ6Ar-bgj2vGU2T_n6K-AnTMhLDxX3QwVkd9lNiqakD3P6IVEsw7qtxaTq_m59sd2B-DlJ6Er_pw3RoBU29ejwTHoI-kPoFg"""

BODY = {
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
        "point": {"lat": 48.22029015850006, "lon": 16.371278701731626},
    },
    "zipCode": None,
    "sort": {"direction": "DESC", "field": "RELEVANCE"},
    "immoItemTypes": ["ESTATE", "PROJECT"],
    "paging": {"size": 200, "page": 1},
}


class NoConnectionError(Exception):
    pass


class RequestObject(Protocol):
    @property
    def url(self) -> str:
        ...

    @property
    def header(self) -> dict[str, str]:
        ...


class PostRequestObject(Protocol):
    @property
    def url(self) -> str:
        ...

    @property
    def header(self) -> dict[str, str]:
        ...

    @property
    def body(self) -> dict[str, str | int]:
        ...


def get_header():
    return {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": BEARER_TOKEN,
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    }


def get_body():
    return json.dumps(BODY)


@dataclass
class ImmoweltRequest:
    url: str = "https://api.immowelt.com/residentialsearch/v1/searches"
    header: dict[str, str] = field(default_factory=get_header)
    body: str = field(default_factory=get_body)


def post_request(obj: PostRequestObject) -> requests.Response:
    try:
        response = requests.post(
            url=obj.url, data=obj.body, headers=obj.header
        )
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        print(response.text)
        raise NoConnectionError(f"HTTP Error: {e.response.status_code}") from e
    except Exception as e:
        raise NoConnectionError(
            f"No connection could be established!\n{e}"
        ) from e
    return response


def main():
    request = ImmoweltRequest()
    response = post_request(request)
    print(response.json())


if __name__ == "__main__":
    main()
