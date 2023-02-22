class WohnungenWien:
    def __init__(self, rows: int = 500, page: int = 1):
        self._rows = rows
        self._page = page

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

    @property
    def page(self) -> int:
        return self._page

    @page.setter
    def page(self, value: int):
        self._page = value

    @property
    def area_id(self) -> int:
        """Area ID denotes what area in Austria. 900 is Wien."""
        return 900

    @property
    def rows(self) -> int:
        return self._rows
