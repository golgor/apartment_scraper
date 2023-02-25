from apartment_scraper.willhaben.parse import parse_willhaben_response
from apartment_scraper.willhaben.request import WohnungenWien

__all__ = ["WohnungenWien", "parse_willhaben_response"]

from time import sleep
from typing import Any, Protocol

import requests


class NoConnectionError(Exception):
    pass


class WillhabenRequest(Protocol):
    @property
    def url(self) -> str:
        ...

    @property
    def params(self) -> dict[str, str | int]:
        ...

    @property
    def header(self) -> dict[str, str]:
        ...

    @property
    def rows(self) -> int:
        ...

    @property
    def page(self) -> int:
        ...

    @page.setter
    def page(self, value: int):
        ...

    @property
    def area_id(self) -> int:
        ...


def get_data(obj: WillhabenRequest) -> list[dict[str, Any]]:
    data: list[dict[str, Any]] = []
    sum = 0
    while True:
        sleep(0.5)
        response = _perform_request(
            url=obj.url, header=obj.header, params=obj.params
        )
        if not response.get("rowsReturned"):
            break

        print(f"Successfull request for page {obj.page}")
        sum += len(response["advertSummaryList"]["advertSummary"])
        print(f"Requested {sum} / {response['rowsFound']}")

        obj.page += 1
        data.extend(response["advertSummaryList"]["advertSummary"])
    return data


def _perform_request(
    url: str, header: dict[str, str], params: dict[str, str | int]
) -> dict[str, Any]:
    try:
        response = requests.get(url=url, headers=header, params=params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        raise NoConnectionError(f"HTTP Error: {e.response.status_code}") from e
    except Exception as e:
        raise NoConnectionError(e) from e
    return response.json()
