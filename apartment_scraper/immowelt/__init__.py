from time import sleep
from typing import Any, Protocol, Self

import httpx
from loguru import logger

# from apartment_scraper.immowelt.parse import parse_immowelt_response
from apartment_scraper.immowelt.request import WohnungenWien


__all__ = ["get_immowelt_token", "WohnungenWien"]


class NoConnectionError(Exception):
    pass


class ImmoweltRequest(Protocol):
    @property
    def url(self: Self) -> str:
        ...

    @property
    def header(self: Self) -> dict[str, str]:
        ...

    @property
    def body(self: Self) -> dict[str, str | int] | str:
        ...

    @property
    def page(self: Self) -> int:
        ...

    @page.setter
    def page(self: Self, value: int) -> None:
        ...


class ImmoweltTokenRequest:
    @property
    def url(self: Self) -> str:
        return "https://api.immowelt.com/auth/oauth/token"

    @property
    def header(self: Self) -> dict[str, str]:
        return {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/x-www-form-urlencoded",
            "authorization": "Basic cmVzaWRlbnRpYWwtc2VhcmNoLXVpOlU4KzhzYn4oO1E0YlsyUXcjaHl3TSlDcTc=",
        }

    @property
    def body(self: Self) -> dict[str, str | int]:
        return {"grant_type": "client_credentials"}


def get_immowelt_token() -> str:
    """Function to get the access token for the immowelt api.

    This is needed later in order to get the data from the api.
    """
    tr = ImmoweltTokenRequest()
    response = _perform_request(
        body=tr.body,
        header=tr.header,
        url=tr.url,
    )
    access_token = response["access_token"]
    return f"Bearer {access_token}"


def _perform_request(
    url: str, header: dict[str, str], body: dict[str, str | int]
) -> dict[str, Any]:
    try:
        response = httpx.post(url=url, data=body, headers=header)
        response.raise_for_status()
    except httpx.HTTPError as e:
        logger.error(response.content.decode("utf-8"))
        raise NoConnectionError from e
    except Exception as e:
        raise NoConnectionError(e) from e
    return response.json()


def get_data(obj: ImmoweltRequest) -> list[dict[str, Any]]:
    data: list[dict[str, Any]] = []
    summed_rows = 0
    while True:
        sleep(0.5)
        response = _perform_request(url=obj.url, header=obj.header, body=obj.body)
        if not response.get("pageElementCount"):
            break

        logger.info(f"Successfull request for page {obj.page}")
        summed_rows += len(response["data"])
        logger.info(f"Requested {summed_rows} / {response['totalCount']}")

        obj.page += 1
        data.extend(response["data"])
    return data
