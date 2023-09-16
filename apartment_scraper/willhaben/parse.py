from enum import Enum
from typing import Any

# from apartment_scraper import Apartment
from apartment_scraper.models import Apartment


class ProductId(Enum):
    UNDEFINED = 0
    PRIVATE_BUY = 100
    PRIVATE_RENTAL = 200
    RENTAL = 227
    PROJECT = 270
    EIGENTUM = 223


def get_attribute_with_name(
    response: dict[str, Any], name: str, fallback: Any
) -> list[str] | Any:
    attributes: list[dict[str, Any]] = response["attributes"]["attribute"]
    return next(
        (
            attribute["values"]
            for attribute in attributes
            if attribute["name"] == name
        ),
        fallback,
    )


def parse_price_attribute(response: dict[str, Any]) -> float:
    try:
        price = get_attribute_with_name(response, "PRICE", 0)[0]
        return float(price)
    except Exception:
        print("Failed to parse the field 'PRICE' for " f"id={response['id']}")
        return 0


def parse_url_attribute(response: dict[str, Any]) -> str:
    try:
        if url := get_attribute_with_name(response, "SEO_URL", "")[0]:
            return f"https://www.willhaben.at/iad/{url}"
        return ""
    except Exception:
        print(
            "Failed to parse the field 'SEO_URL' for " f"id={response['id']}"
        )
        return ""


def parser_advertiser_attribute(response: dict[str, Any]) -> str:
    try:
        return response["advertiserInfo"]["label"] or ""
    except Exception:
        print("Failed parse AdvertiserInfo for " f"id={response['id']}")
        return ""


def parse_post_code_attribute(response: dict[str, Any]) -> str:
    try:
        return get_attribute_with_name(response, "POSTCODE", "")[0]
    except Exception:
        print(
            "Failed to parse the field 'POSTCODE' for " f"id={response['id']}"
        )
        return ""


def parse_id_attribute(response: dict[str, Any]) -> str:
    apartment_id: str = response["id"]
    return apartment_id


def parse_area_attribute(response: dict[str, Any]) -> float:
    try:
        area = get_attribute_with_name(response, "ESTATE_SIZE/LIVING_AREA", 0)[
            0
        ]
        return float(area)
    except Exception:
        print(
            "Failed to parse the field 'ESTATE_SIZE/LIVING_AREA' for "
            f"id={response['id']}"
        )
        return 0


def parse_room_attribute(response: dict[str, Any]) -> float:
    try:
        area: str = get_attribute_with_name(response, "NUMBER_OF_ROOMS", 0)[0]
        return float(area)
    except Exception:
        print(
            "Failed to parse the field 'NUMBER_OF_ROOMS' for "
            f"id={response['id']}"
        )
        return 0


def parse_floor_attribute(response: dict[str, Any]) -> float:
    try:
        floor: str = get_attribute_with_name(response, "FLOOR", 0)[0]
        return float(floor)
    except Exception:
        print("Failed to parse the field 'FLOOR' for " f"id={response['id']}")
        return 0


def parse_rent_attribute(response: dict[str, Any]) -> float:
    try:
        rent: str = get_attribute_with_name(
            response, "RENT/PER_MONTH_LETTINGS", 0
        )[0]
        return round(float(rent), 2)
    except Exception:
        print("Failed to parse the field 'RENT' for " f"id={response['id']}")
        return 0


def parse_address_attribute(response: dict[str, Any]) -> str:
    try:
        address: str = get_attribute_with_name(response, "ADDRESS", 0)[0]
        return address
    except Exception:
        print(
            "Failed to parse the field 'ADDRESS' for " f"id={response['id']}"
        )
        return ""


def parse_free_area_attribute(response: dict[str, Any]) -> int:
    try:
        free_area: list[str] = get_attribute_with_name(
            response, "FREE_AREA/FREE_AREA_AREA_TOTAL", 0
        )
        return int(free_area[0])
    except Exception:
        print(
            "Failed to parse the field 'FREE_AREA' for " f"id={response['id']}"
        )
        return 0


def parse_free_area_type_name_attribute(response: dict[str, Any]) -> list[str]:
    try:
        free_area_type: list[str] = get_attribute_with_name(
            response, "FREE_AREA_TYPE_NAME", []
        )
        return free_area_type
    except Exception:
        print(
            "Failed to parse the field 'FREE_AREA_TYPE_NAME' for "
            f"id={response['id']}"
        )
        return []


def parse_status_attribute(response: dict[str, Any]) -> bool:
    active: str = response["advertStatus"]["id"]
    return active == "active"


def parse_image_urls_attribute(response: dict[str, Any]) -> list[str]:
    # sourcery skip: use-named-expression
    try:
        urls: str = get_attribute_with_name(response, "ALL_IMAGE_URLS", "")[0]
        if urls:
            return [
                f"https://cache.willhaben.at/mmo/{url}"
                for url in urls.split(";")
            ]
        else:
            return []
    except Exception:
        print(
            "Failed to parse the field 'ALL_IMAGE_URLS' for "
            f"id={response['id']}"
        )
        return []


def parse_coordinates_attribute(response: dict[str, Any]) -> str:
    try:
        coordinates: str = get_attribute_with_name(
            response, "COORDINATES", ""
        )[0]
        return coordinates
    except Exception:
        print(
            "Failed to parse the field 'COORDINATES' for "
            f"id={response['id']}"
        )
        return ""


def parse_product_id_attribute(response: dict[str, Any]) -> str:
    try:
        product_id: str = get_attribute_with_name(response, "PRODUCT_ID", "")[
            0
        ]
        return ProductId(int(product_id)).name.lower()
    except ValueError as e:
        if local_product_id := locals().get("product_id", None):
            print(
                f"Failed to convert product_id={local_product_id} to ProductId enum"
            )
            return str(local_product_id)
        else:
            return ""
    except Exception as e:
        print(
            "Failed to parse the field 'PRODUCT_ID' for "
            f"id={response['id']}"
        )
        return ""


def parse_location_attribute(response: dict[str, Any]) -> str:
    try:
        location: str = get_attribute_with_name(response, "LOCATION", "")[0]
        return location
    except Exception:
        print(
            "Failed to parse the field 'LOCATION' for " f"id={response['id']}"
        )
        return ""


def parse_property_type_attribute(response: dict[str, Any]) -> str:
    try:
        property_type: str = get_attribute_with_name(
            response, "PROPERTY_TYPE", ""
        )[0]
        return property_type
    except Exception:
        print(
            "Failed to parse the field 'PROPERTY_TYPE' for "
            f"id={response['id']}"
        )
        return ""


def calc_rent_per_area(response: dict[str, Any]) -> float:
    try:
        rent = parse_rent_attribute(response)
        area = parse_area_attribute(response)
        return round(float(rent) / float(area), 2)
    except Exception:
        print("Failed to calculate rent/area for " f"id={response['id']}")
        return 0


def calc_price_per_area(response: dict[str, Any]) -> float:
    try:
        rent = parse_price_attribute(response)
        area = parse_area_attribute(response)
        return round(float(rent) / float(area), 2)
    except Exception:
        print("Failed to calculate price/area for " f"id={response['id']}")
        return 0


def parse_willhaben_response(
    elements: list[dict[str, Any]]
) -> list[Apartment]:
    apartment_list: list[Apartment] = [
        Apartment(
            apartment_id=parse_id_attribute(element),
            product_id=parse_product_id_attribute(element),
            property_type=parse_property_type_attribute(element),
            status=parse_status_attribute(element),
            price=parse_price_attribute(element),
            price_per_area=calc_price_per_area(element),
            area=parse_area_attribute(element),
            url=parse_url_attribute(element),
            post_code=parse_post_code_attribute(element),
            location=parse_location_attribute(element),
            rooms=parse_room_attribute(element),
            floor=parse_floor_attribute(element),
            address=parse_address_attribute(element),
            image_urls=parse_image_urls_attribute(element),
            coordinates=parse_coordinates_attribute(element),
            free_area_type=parse_free_area_type_name_attribute(element),
            free_area=parse_free_area_attribute(element),
            advertiser=parser_advertiser_attribute(element),
        )
        for element in elements
    ]
    return apartment_list
