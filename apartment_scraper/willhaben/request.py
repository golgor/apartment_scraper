from typing import Any

import requests


class NoConnectionError(Exception):
    pass


class Requester:
    def __init__(self, rows: int = 200, area_id: int = 900, page: int = 1):
        self.rows = rows
        self.area_id = area_id
        self.page = page
        self.sum = 0

    @property
    def url(self) -> str:
        return (
            "https://www.willhaben.at/webapi/iad/search/atz/seo/immobilien/"
            "eigentumswohnung/eigentumswohnung-angebote"
        )

    @property
    def params(self) -> dict[str, str | int]:
        return {"rows": self.rows, "areaId": self.area_id, "page": self.page}

    @property
    def header(self) -> dict[str, str]:
        return {
            "accept": "application/json",
            "x-wh-client": (
                "api@willhaben.at;responsive_web;server;1.0.0;desktop"
            ),
        }

    def __iter__(self):
        return self

    def __next__(self) -> list[dict[str, Any]]:
        response = self._perform_request()
        if not response.get("rowsReturned"):
            raise StopIteration

        print(f"Successfull request for page {self.page}")
        self.sum += len(response["advertSummaryList"]["advertSummary"])
        print(f"Requested {self.sum} / {response['rowsFound']}")

        self.page += 1
        return response["advertSummaryList"]["advertSummary"]

    def _perform_request(self) -> dict[str, Any]:
        try:
            response = requests.get(
                url=self.url, headers=self.header, params=self.params
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise NoConnectionError(
                f"HTTP Error: {e.response.status_code}"
            ) from e
        except Exception as e:
            raise NoConnectionError(e) from e
        return response.json()
