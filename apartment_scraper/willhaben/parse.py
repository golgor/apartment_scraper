from enum import Enum, StrEnum
from typing import Any

from apartment_scraper import Apartment, Site
from apartment_scraper.data_exporter import DataExporter
from apartment_scraper.data_loader import DataLoader


class ProductId(Enum):
    UNDEFINED = 0
    NEUBAU = 270
    EIGENTUMSWOHNUNG = 223


class PostCodeWien(StrEnum):
    UNDEFINED = "0"
    INNERE_STADT = "1010"
    LEOPOLDSTADT = "1020"
    LANDSTRASSE = "1030"
    WIEDEN = "1040"
    MARGARETEN = "1050"
    MARIAHILF = "1060"
    NEUBAU = "1070"
    JOSEFSTADT = "1080"
    ALSERGRUND = "1090"
    FAVORITEN = "1100"
    SIMMERING = "1110"
    MEIDLING = "1120"
    HIETZING = "1130"
    PENZING = "1140"
    RUDOLFSHEIM_FUNFHAUS = "1150"
    OTTAKRING = "1160"
    HERNALS = "1170"
    WÄHRING = "1180"
    DÖBLING = "1190"
    BRIGITTENAU = "1200"
    FLORIDSDORF = "1210"
    DONAUSTADT = "1220"
    LIESING = "1230"


class FieldParser:
    def __init__(self, response: dict[str, Any]):
        self.response = response
        self.attributes: list[dict[str, Any]] = response["attributes"][
            "attribute"
        ]

    def get_attr(self, name: str, fallback: Any = None) -> Any:
        # sourcery skip: use-next, useless-else-on-loop
        for attribute in self.attributes:
            if attribute["name"] == name:
                return attribute["values"][0]
        else:
            return fallback

    @property
    def price(self) -> float:
        try:
            price = self.get_attr("PRICE", 0)
            return float(price)
        except Exception:
            print(
                "Failed to parse the field 'PRICE' for "
                f"id={self.response['id']}, "
                f"url={self.url}"
            )
            return 0

    @property
    def area(self) -> float:
        try:
            return float(self.get_attr("ESTATE_SIZE/LIVING_AREA", 0))
        except Exception:
            print(
                "Failed to parse the field 'ESTATE_SIZE/LIVING_AREA' for "
                f"id={self.response['id']}, "
                f"url={self.url}"
            )
            return 0

    @property
    def url(self) -> str:
        try:
            if url := self.get_attr("SEO_URL", ""):
                return f"https://www.willhaben.at/iad/{url}"
            else:
                raise ValueError
        except Exception:
            print(
                "Failed to parse the field 'SEO_URL' for "
                f"id={self.response['id']}"
            )
            return ""

    @property
    def product_id(self) -> ProductId:
        return ProductId(self.response.get("productId", 0))

    @property
    def postcode(self) -> PostCodeWien:
        return PostCodeWien(self.get_attr(name="POSTCODE", fallback="0"))

    @property
    def rooms(self) -> int:
        return int(self.get_attr("NUMBER_OF_ROOMS", 0))

    @property
    def active(self) -> bool:
        return self.response["advertStatus"]["id"] == "active"

    @property
    def floor(self) -> int:
        try:
            return int(self.get_attr("FLOOR", 0))
        except Exception:
            print(
                "Failed to parse the field 'FLOOR' for "
                f"id={self.response['id']}"
            )
            return 0

    @property
    def id(self) -> str:
        return self.response["id"]


def parse_willhaben_response(
    responses: list[dict[str, Any]]
) -> list[Apartment]:
    apartment_list: list[Apartment] = []
    for response in responses:
        parser = FieldParser(response=response)
        if parser.active:
            apartment_list.append(
                Apartment(
                    id=parser.id,
                    price=parser.price,
                    area=parser.area,
                    url=parser.url,
                    post_code=parser.postcode,
                    rooms=parser.rooms,
                    floor=parser.floor,
                )
            )
    return apartment_list


def main():
    file_name = "willhaben_2023-02-17.json"
    dl = DataLoader(site=Site.WILLHABEN)
    de = DataExporter(site=Site.WILLHABEN)
    raw_data = dl.load_raw_data(file_name)
    apartments = parse_willhaben_response(raw_data)
    # export_apartments_to_csv(apartments)
    # de.export_excel("test.csv", apartments)
    de.export_json(file_name, apartments)
    # export_to_json(apartments, file_name)
    # apartments = dl.load_clean_data(filename=file_name)
    # export_apartments_to_csv(apartments)


if __name__ == "__main__":
    main()
