from enum import Enum
from typing import Any


class NoConnectionError(Exception):
    pass


class MietWohnungen:
    def __init__(self, area_id: Enum, rows: int = 200, page: int = 1):
        self._rows = rows
        self._page = page
        self._area_id = area_id

    @property
    def url(self) -> str:
        return "https://www.willhaben.at/webapi/iad/search/atz/seo/immobilien/mietwohnungen/mietwohnung-angebote"

    @property
    def params(self) -> dict[str, Any]:
        return {
            "rows": self.rows,
            "areaId": self.area_id,
            "page": self.page,
        }

    @property
    def header(self) -> dict[str, str]:
        return {
            "accept": "application/json",
            "x-wh-client": (
                "api@willhaben.at;responsive_web;server;1.0.0;desktop"
            ),
        }

    @property
    def page(self) -> int:
        return self._page

    @page.setter
    def page(self, value: int) -> None:
        self._page = value

    @property
    def area_id(self) -> int:
        """Area ID denotes what area in Austria. 900 is Wien."""
        area_id_value: int = self._area_id.value
        return area_id_value

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def name(self) -> str:
        string = str(self._area_id)[1:]
        area_string = string.replace(".", "_").lower()
        return f"miet_wohnungen_{area_string}"


class KaufWohnungen:
    def __init__(self, area_id: Enum, rows: int = 200, page: int = 1):
        self._rows = rows
        self._page = page
        self._area_id = area_id

    @property
    def url(self) -> str:
        return (
            "https://www.willhaben.at/webapi/iad/search/atz/seo/immobilien/"
            "eigentumswohnung/eigentumswohnung-angebote"
        )

    @property
    def params(self) -> dict[str, Any]:
        return {"rows": self.rows, "areaId": self.area_id, "page": self.page}

    @property
    def header(self) -> dict[str, str]:
        return {
            "accept": "application/json",
            "x-wh-client": (
                "api@willhaben.at;responsive_web;server;1.0.0;desktop"
            ),
        }

    @property
    def page(self) -> int:
        return self._page

    @page.setter
    def page(self, value: int) -> None:
        self._page = value

    @property
    def area_id(self) -> int:
        """Area ID denotes what area in Austria. 900 is Wien."""
        area_id_value: int = self._area_id.value
        return area_id_value

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def name(self) -> str:
        string = str(self._area_id)[1:]
        area_string = string.replace(".", "_").lower()
        return f"kauf_wohnungen_{area_string}"
