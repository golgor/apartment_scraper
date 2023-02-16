import json
from typing import Any

from apartment_scraper import pkg_path


class WillhabenApartment:
    def __init__(self, api_response: dict[str, Any]):
        self.api_response = api_response
        self.parse_basic_data()
        self.parse_attributes()

    def parse_basic_data(self):
        self._status = self.api_response["advertStatus"]
        self._description = self.api_response["description"]

    def parse_attributes(self) -> None:
        attributes: list[dict[str, Any]] = self.api_response["attributes"][
            "attribute"
        ]
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
        self.attributes = {
            key: value[0] if len(value) == 1 else value
            for key, value in filtered_attributes.items()
        }

    @property
    def url(self) -> str:
        return f"https://www.willhaben.at/iad/{self.attributes['SEO_URL']}"

    @property
    def status(self) -> str:
        return self._status["id"]

    @property
    def description(self) -> str:
        return self._description

    @property
    def rooms(self) -> int:
        try:
            return int(self.attributes["NUMBER_OF_ROOMS"])
        except KeyError:
            return 0

    @property
    def area(self) -> int:
        try:
            return int(self.attributes["ESTATE_SIZE/LIVING_AREA"])
        except KeyError:
            return 0

    @property
    def price(self) -> int:
        try:
            return int(float(self.attributes["PRICE"]))
        except KeyError:
            return 0

    @property
    def price_per_area(self) -> int:
        return (
            round(self.price / self.area)
            if (self.area > 0 and self.price > 0)
            else 0
        )

    def __repr__(self) -> str:
        return f"Location: {self.attributes['LOCATION']}, Size: {self.attributes['NUMBER_OF_ROOMS']}, Area: {self.attributes['ESTATE_SIZE']}"

    def pretty_print_attributes(self):
        print(json.dumps(self.attributes, indent=2))


def import_json(filename: str) -> dict[str, Any]:
    # sourcery skip: instance-method-first-arg-name
    filepath = pkg_path.joinpath("data", filename)
    with open(filepath, "r") as f:
        return json.load(f)


def main():
    raw_data = import_json("willhaben_wien.json")
    api_apartments = raw_data["advertSummaryList"]["advertSummary"]
    parsed_apartments = [WillhabenApartment(item) for item in api_apartments]
    for apartment in parsed_apartments:
        print(apartment.price_per_area)
        print(apartment.url)


if __name__ == "__main__":
    main()
