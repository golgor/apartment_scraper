from typing import Protocol

import requests


class NoConnectionError(Exception):
    pass


class RequestObject(Protocol):
    @property
    def url(self) -> str:
        ...

    @property
    def header(self) -> dict[str, str]:
        ...

    @property
    def params(self) -> dict[str, str | int]:
        ...


def get_request(obj: RequestObject) -> requests.Response:
    try:
        response = requests.get(
            url=obj.url, headers=obj.header, params=obj.params
        )
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        raise NoConnectionError(f"HTTP Error: {e.response.status_code}") from e
    except Exception as e:
        raise NoConnectionError(
            f"No connection could be established!\n{e}"
        ) from e
    return response
