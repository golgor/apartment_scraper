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



@dataclass
class Apartment:
    # area: float
    price: float
    url: str
    # coordinates: tuple[float, float]
    rooms: int
    # floor: int
    # address: str
    # broker: str = ""

    # @property
    # def price_per_area(self):
    #     return self.price / self.area


def get_status(response: dict[str, Any]) -> str:
    return response["advertStatus"]["id"]


def get_attributes(response: dict[str, Any]) -> dict[str, Any]:
    attributes: list[dict[str, Any]] = response["attributes"]["attribute"]
    keys_of_interest = [
        "LOCATION",
        "POSTCODE",
        "STATE",
        "ORGNAME",
        "ESTATE_SIZE/LIVING_AREA",
        "DISTRICT",
        "LOCATION_QUALITY",
        "FLOOR",
        "PROPERTY_TYPE",
        "NUMBER_OF_ROOMS",
        "SEO_URL",
        "FREE_AREA_TYPE",
        "FREE_AREA_TYPE_NAME",
        "FREE_AREA/FREE_AREA_AREA_TOTAL",
        "PUBLISHED_String",
        "ESTATE_PRICE/PRICE_SUGGESTION",
        "ESTATE_SIZE/USEABLE_AREA",
        "ADDRESS",
        "COORDINATES",
        "PRICE",
        "PRICE_FOR_DISPLAY",
        "ESTATE_SIZE",
    ]
    filtered_attributes = {
        item["name"]: item["values"]
        for item in attributes
        if item["name"] in keys_of_interest
    }
    # Unpacking values if in a list and only one element
    return {
        key: value[0] if len(value) == 1 else value
        for key, value in filtered_attributes.items()
    }


def parse_price(attributes: dict[str, Any]) -> float:
    return float(attributes.get("PRICE", 0))


def parse_willhaben_response(raw_responses: dict[str, Any]) -> list[Apartment]:
    responses = raw_responses["advertSummaryList"]["advertSummary"]
    apartment_list: list[Apartment] = []
    for response in responses:
        if get_status(response) == "active":
            attributes = get_attributes(response)
            # Add parsing functions for each attribute, sometimes they don't
            # exist, sometimes under one or several attributes or not
            # available.
            parse_price(attributes=attributes)
            apartment_list.append(
                Apartment(
                    # area=float(attributes["ESTATE_SIZE/LIVING_AREA"]),
                    price=parse_price(attributes),
                    url=f"https://www.willhaben.at/iad/{attributes['SEO_URL']}",
                    # coordinates=attributes["COORDINATES"],
                    rooms=int(attributes["NUMBER_OF_ROOMS"]),
                    # floor=int(attributes["FLOOR"]),
                    # address=attributes["ADDRESS"],
                    # broker=attributes["ORGNAME"],
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
