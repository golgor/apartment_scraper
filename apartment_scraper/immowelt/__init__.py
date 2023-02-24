from typing import Protocol

import requests


class NoConnectionError(Exception):
    pass


class ImmoweltRequest(Protocol):
    @property
    def url(self) -> str:
        ...

    @property
    def header(self) -> dict[str, str]:
        ...

    @property
    def body(self) -> dict[str, str | int] | str:
        ...


def post_request(obj: ImmoweltRequest) -> requests.Response:
    try:
        response = requests.post(
            url=obj.url, data=obj.body, headers=obj.header
        )
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        print(e)
        raise NoConnectionError(f"HTTP Error: {e.response.status_code}") from e
    except Exception as e:
        raise NoConnectionError(
            f"No connection could be established!\n{e}"
        ) from e
    return response
