import json
from dataclasses import dataclass, field
from enum import Enum, StrEnum
from typing import Any

from apartment_scraper import pkg_path


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

    def get_attr(self, name: str) -> list[str]:
        for attribute in self.attributes:
            if attribute.get("name") == name:
                return attribute["values"]
        raise KeyError(f"Attribute {name} not found!")

    @property
    def price(self) -> float:
        try:
            return float(self.get_attr("PRICE")[0])
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
            return float(self.get_attr("ESTATE_SIZE/LIVING_AREA")[0])
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
            return (
                f"https://www.willhaben.at/iad/{self.get_attr('SEO_URL')[0]}"
            )
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
        try:
            postcode = self.get_attr("POSTCODE")[0]
            return PostCodeWien(postcode)
        except KeyError as e:
            print(e)
            return PostCodeWien("0")

    @property
    def rooms(self) -> int:
        try:
            return int(self.get_attr("NUMBER_OF_ROOMS")[0])
        except Exception as e:
            print(e)
            return 0

    @property
    def active(self) -> bool:
        return self.response["advertStatus"]["id"] == "active"


@dataclass
class Apartment:
    area: float
    price: float
    url: str = field(repr=False)
    # coordinates: tuple[float, float]
    rooms: int
    # floor: int
    # address: str
    # broker: str = ""
    post_code: str

    # @property
    # def price_per_area(self):
    #     try:
    #         return self.price / self.area
    #     except Exception:
    #         print("Division by zero")
    #         return 0


def get_status(response: dict[str, Any]) -> str:
    return response["advertStatus"]["id"]


def parse_willhaben_response(
    responses: list[dict[str, Any]]
) -> list[Apartment]:
    apartment_list: list[Apartment] = []
    for response in responses:
        parser = FieldParser(response=response)
        if parser.active:
            apartment_list.append(
                Apartment(
                    price=parser.price,
                    area=parser.area,
                    url=parser.url,
                    post_code=parser.postcode,
                    rooms=parser.rooms,
                )
            )
    return apartment_list


def import_json(filename: str) -> dict[str, Any]:
    filepath = pkg_path.joinpath("data", filename)
    with open(filepath, "r") as f:
        return json.load(f)


def main():
    raw_data = import_json("willhaben_wien.json")
    apartments = parse_willhaben_response(raw_data)
    for apartment in apartments:
        print(apartment)


if __name__ == "__main__":
    main()
