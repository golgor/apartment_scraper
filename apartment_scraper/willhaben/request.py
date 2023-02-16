class WillhabenRequestObject:
    def __init__(self):
        pass

    @property
    def url(self) -> str:
        return (
            "https://www.willhaben.at/webapi/iad/search/atz/seo/immobilien/"
            "eigentumswohnung/eigentumswohnung-angebote"
        )

    @property
    def params(self) -> dict[str, str | int]:
        return {"rows": 10, "areaId": 900, "page": 1}

    @property
    def header(self) -> dict[str, str]:
        return {
            "accept": "application/json",
            "x-wh-client": (
                "api@willhaben.at;responsive_web;server;1.0.0;desktop"
            ),
        }
