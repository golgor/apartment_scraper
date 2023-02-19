import csv
import json
from dataclasses import dataclass, field
from enum import Enum, StrEnum
from typing import Any, Iterable

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
        return self.get_attr("FLOOR", 0)

    @property
    def id(self) -> str:
        return self.response["id"]


@dataclass
class Apartment:
    id: str
    area: float
    price: float
    url: str = field(repr=False)
    # coordinates: tuple[float, float]
    rooms: int
    floor: int
    # address: str
    # broker: str = ""
    post_code: str

    @property
    def price_per_area(self):
        try:
            return round(self.price / self.area, 0)
        except Exception:
            print("Division by zero")
            return 0

    @property
    def columns(self) -> Iterable[str]:
        return [
            "id",
            "area",
            "price",
            "url",
            "rooms",
            "post_code",
            "price_per_area",
        ]

    def to_json(self):
        return {
            "area": self.area,
            "price": self.price,
            "url": self.url,
            "rooms": self.rooms,
            "floor": self.floor,
            "post_code": self.post_code,
        }


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


def export_apartments_to_csv(apartments: list[Apartment]) -> None:
    # Example.csv gets created in the current working directory
    with open("Example.csv", "w", newline="\n") as csvfile:
        my_writer = csv.writer(csvfile, delimiter=",")
        my_writer.writerow(apartments[0].columns)
        for apartment in apartments:
            my_writer.writerow(
                (
                    apartment.area,
                    apartment.price,
                    apartment.url,
                    apartment.rooms,
                    apartment.post_code,
                    apartment.price_per_area,
                )
            )


def export_to_json(apartments: list[Apartment], filename: str) -> None:
    apartment_dict = {
        apartment.id: apartment.to_json() for apartment in apartments
    }
    with open(filename, "w") as f:
        f.write(json.dumps(apartment_dict, indent=2))


def import_json(filename: str) -> list[dict[str, Any]]:
    filepath = pkg_path.joinpath("data", filename)
    with open(filepath, "r") as f:
        return json.load(f)


def main():
    file_name = "willhaben_2023-02-19.json"
    raw_data = import_json(file_name)
    apartments = parse_willhaben_response(raw_data)
    # export_apartments_to_csv(apartments)
    export_to_json(apartments, f"cleaned_{file_name}")


if __name__ == "__main__":
    main()
