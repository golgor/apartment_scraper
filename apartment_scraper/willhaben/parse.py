from enum import Enum
from typing import Any

# from apartment_scraper import Apartment
from apartment_scraper.models import ApartmentBuy, ApartmentRent


class ProductId(Enum):
    UNDEFINED = 0
    NEUBAU = 270
    EIGENTUMSWOHNUNG = 223


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
            return ""
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
    def postcode(self) -> str:
        return self.get_attr(name="POSTCODE", fallback="0")

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

    @property
    def price_per_area(self) -> float:
        try:
            return self.price / self.area
        except Exception:
            print(
                "Failed to calculate price_per_area' for "
                f"id={self.response['id']}"
            )
            return 0

    @property
    def image_urls(self) -> list[str]:
        try:
            return self.get_attr("ALL_IMAGE_URLS", "")
        except Exception:
            print(
                "Failed to parse ALL_IMAGE_URLS' for "
                f"id={self.response['id']}"
            )
            return [""]

    @property
    def rent(self) -> float:
        try:
            price = self.get_attr("RENT/PER_MONTH_LETTINGS", 0)
            return round(float(price), 2)
        except Exception:
            print(
                "Failed to parse the field 'PRICE' for "
                f"id={self.response['id']}, "
                f"url={self.url}"
            )
            return 0

    @property
    def rent_per_area(self) -> float:
        try:
            return round(self.rent / self.area, 2)
        except Exception:
            print(
                "Failed to calculate price_per_area' for "
                f"id={self.response['id']}"
            )
            return 0

    @property
    def coordinates(self) -> str | None:
        try:
            return self.get_attr("COORDINATES", None)
        except Exception:
            print(
                "Failed to calculate price_per_area' for "
                f"id={self.response['id']}"
            )
            return None

    @property
    def free_area_type(self) -> str | None:
        try:
            return self.get_attr("FREE_AREA_TYPE_NAME", None)
        except Exception:
            print(
                "Failed to calculate price_per_area' for "
                f"id={self.response['id']}"
            )
            return None

    @property
    def free_area(self) -> int | None:
        try:
            area = int(self.get_attr("FREE_AREA/FREE_AREA_AREA_TOTAL", 0))
            return None if area == 0 else area
        except Exception:
            print(
                "Failed to calculate price_per_area' for "
                f"id={self.response['id']}"
            )
            return None

    @property
    def address(self) -> str:
        try:
            return self.get_attr("ADDRESS", "")
        except Exception:
            print("Failed parse ADDRESS for " f"id={self.response['id']}")
            return ""


def parse_willhaben_buy_response(
    elements: list[dict[str, Any]]
) -> list[ApartmentBuy]:
    apartment_list: list[ApartmentBuy] = []
    for element in elements:
        parser = FieldParser(response=element)
        if parser.active:
            apartment_list.append(
                ApartmentBuy(
                    apartment_id=parser.id,
                    price=parser.price,
                    area=parser.area,
                    url=parser.url,
                    post_code=parser.postcode,
                    rooms=parser.rooms,
                    floor=parser.floor,
                    price_per_area=parser.price_per_area,
                    image_urls=parser.image_urls,
                    site="willhaben",
                )
            )
    return apartment_list


def parse_willhaben_rent_response(
    elements: list[dict[str, Any]]
) -> list[ApartmentRent]:
    apartment_list: list[ApartmentRent] = []
    for element in elements:
        parser = FieldParser(response=element)
        if parser.active:
            apartment_list.append(
                ApartmentRent(
                    apartment_id=parser.id,
                    rent=parser.rent,
                    area=parser.area,
                    url=parser.url,
                    post_code=parser.postcode,
                    rooms=parser.rooms,
                    floor=parser.floor,
                    address=parser.address,
                    rent_per_area=parser.rent_per_area,
                    image_urls=parser.image_urls,
                    coordinates=parser.coordinates,
                    free_area_type=parser.free_area_type,
                    free_area=parser.free_area,
                    site="willhaben",
                )
            )
    return apartment_list
