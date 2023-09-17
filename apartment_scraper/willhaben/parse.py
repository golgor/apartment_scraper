from enum import Enum
from typing import Any

from loguru import logger

# from apartment_scraper import Apartment
from apartment_scraper.models import Apartment


class ProductId(Enum):
    """Enum for the product id of an apartment."""

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
        (attribute["values"] for attribute in attributes if attribute["name"] == name),
        fallback,
    )


def parse_price_attribute(response: dict[str, Any]) -> float:
    """Parses the 'PRICE' attribute from a response dictionary and returns it as a float.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        float: The parsed 'PRICE' attribute as a float.
    """
    try:
        price = get_attribute_with_name(response, "PRICE", 0)[0]
        return float(price)
    except Exception:
        logger.warning(f"Failed to parse the field 'PRICE' for id={response['id']}")
        return 0


def parse_url_attribute(response: dict[str, Any]) -> str:
    """Parses the 'SEO_URL' attribute from a response dictionary and returns it as a formatted URL string.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        str: The parsed 'SEO_URL' attribute as a formatted URL string.
    """
    try:
        if url := get_attribute_with_name(response, "SEO_URL", "")[0]:
            return f"https://www.willhaben.at/iad/{url}"
        return ""
    except Exception:
        logger.warning(f"Failed to parse the field 'SEO_URL' for id={response['id']}")
        return ""


def parser_advertiser_attribute(response: dict[str, Any]) -> str:
    try:
        return response["advertiserInfo"]["label"] or ""
    except Exception:
        logger.warning(f"Failed parse AdvertiserInfo for id={response['id']}")
        return ""


def parse_post_code_attribute(response: dict[str, Any]) -> str:
    try:
        return get_attribute_with_name(response, "POSTCODE", "")[0]
    except Exception:
        logger.warning(f"Failed to parse the field 'POSTCODE' for id={response['id']}")
        return ""


def parse_id_attribute(response: dict[str, Any]) -> str:
    apartment_id: str = response["id"]
    return apartment_id


def parse_area_attribute(response: dict[str, Any]) -> float:
    try:
        area = get_attribute_with_name(response, "ESTATE_SIZE/LIVING_AREA", 0)[0]
        return float(area)
    except Exception:
        logger.warning(
            "Failed to parse the field 'ESTATE_SIZE/LIVING_AREA' for "
            f"id={response['id']}"
        )
        return 0


def parse_room_attribute(response: dict[str, Any]) -> float:
    try:
        area: str = get_attribute_with_name(response, "NUMBER_OF_ROOMS", 0)[0]
        return float(area)
    except Exception:
        logger.warning(
            "Failed to parse the field 'NUMBER_OF_ROOMS' for " f"id={response['id']}"
        )
        return 0


def parse_floor_attribute(response: dict[str, Any]) -> float:
    try:
        floor: str = get_attribute_with_name(response, "FLOOR", 0)[0]
        return float(floor)
    except Exception:
        logger.warning(f"Failed to parse the field 'FLOOR' for id={response['id']}")
        return 0


def parse_rent_attribute(response: dict[str, Any]) -> float:
    try:
        rent: str = get_attribute_with_name(response, "RENT/PER_MONTH_LETTINGS", 0)[0]
        return round(float(rent), 2)
    except Exception:
        logger.warning(f"Failed to parse the field 'RENT' for id={response['id']}")
        return 0


def parse_address_attribute(response: dict[str, Any]) -> str:
    try:
        address: str = get_attribute_with_name(response, "ADDRESS", 0)[0]
    except Exception:
        logger.warning(f"Failed to parse the field 'ADDRESS' for id={response['id']}")
        return ""
    return address


def parse_free_area_attribute(response: dict[str, Any]) -> int:
    try:
        free_area: list[str] = get_attribute_with_name(
            response, "FREE_AREA/FREE_AREA_AREA_TOTAL", 0
        )
        return int(free_area[0])
    except Exception:
        logger.warning(f"Failed to parse the field 'FREE_AREA' for id={response['id']}")
        return 0


def parse_free_area_type_name_attribute(response: dict[str, Any]) -> list[str]:
    try:
        free_area_type: list[str] = get_attribute_with_name(
            response, "FREE_AREA_TYPE_NAME", []
        )
    except Exception:
        logger.warning(
            "Failed to parse the field 'FREE_AREA_TYPE_NAME' for "
            f"id={response['id']}"
        )
        return []
    return free_area_type


def parse_status_attribute(response: dict[str, Any]) -> bool:
    active: str = response["advertStatus"]["id"]
    return active == "active"


def parse_image_urls_attribute(response: dict[str, Any]) -> list[str]:
    # sourcery skip: use-named-expression
    try:
        urls: str = get_attribute_with_name(response, "ALL_IMAGE_URLS", "")[0]
        if urls:
            return [f"https://cache.willhaben.at/mmo/{url}" for url in urls.split(";")]
        else:
            return []
    except Exception:
        logger.warning(
            "Failed to parse the field 'ALL_IMAGE_URLS' for " f"id={response['id']}"
        )
        return []


def parse_coordinates_attribute(response: dict[str, Any]) -> str:
    try:
        coordinates: str = get_attribute_with_name(response, "COORDINATES", "")[0]
    except Exception:
        logger.warning(
            "Failed to parse the field 'COORDINATES' for " f"id={response['id']}"
        )
        return ""
    return coordinates


def parse_product_id_attribute(response: dict[str, Any]) -> str:
    try:
        product_id: str = get_attribute_with_name(response, "PRODUCT_ID", "")[0]
        return ProductId(int(product_id)).name.lower()
    except ValueError:
        if local_product_id := locals().get("product_id", None):
            logger.warning(
                f"Failed to convert product_id={local_product_id} to ProductId enum"
            )
            return str(local_product_id)
        else:
            return ""
    except Exception:
        logger.warning(
            "Failed to parse the field 'PRODUCT_ID' for " f"id={response['id']}"
        )
        return ""


def parse_location_attribute(response: dict[str, Any]) -> str:
    try:
        location: str = get_attribute_with_name(response, "LOCATION", "")[0]
        return location
    except Exception:
        logger.warning(f"Failed to parse the field 'LOCATION' for id={response['id']}")
        return ""


def parse_property_type_attribute(response: dict[str, Any]) -> str:
    try:
        property_type: str = get_attribute_with_name(response, "PROPERTY_TYPE", "")[0]
        return property_type
    except Exception:
        logger.warning(
            "Failed to parse the field 'PROPERTY_TYPE' for " f"id={response['id']}"
        )
        return ""


def calc_rent_per_area(response: dict[str, Any]) -> float:
    try:
        rent = parse_rent_attribute(response)
        area = parse_area_attribute(response)
        return round(float(rent) / float(area), 2)
    except Exception:
        logger.warning(f"Failed to calculate rent/area for id={response['id']}")
        return 0


def calc_price_per_area(response: dict[str, Any]) -> float:
    try:
        rent = parse_price_attribute(response)
        area = parse_area_attribute(response)
        return round(float(rent) / float(area), 2)
    except Exception:
        logger.warning(f"Failed to calculate price/area for id={response['id']}")
        return 0


def parse_willhaben_response(elements: list[dict[str, Any]]) -> list[Apartment]:
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


def parse_apartment(data_dict: dict[str, Any]) -> Apartment:
    """Parse an Apartment object from a dictionary.

    The data_dict is typically a dictionary containing the response from willhaben with raw data about apartements.

    Args:
        data_dict (dict[str, Any]): A Dictionary with keys describing a dictionary.

    Returns:
        Apartment: An Apartment object.
    """
    return Apartment(
        apartment_id=parse_id_attribute(data_dict),
        product_id=parse_product_id_attribute(data_dict),
        property_type=parse_property_type_attribute(data_dict),
        status=parse_status_attribute(data_dict),
        price=parse_price_attribute(data_dict),
        price_per_area=calc_price_per_area(data_dict),
        area=parse_area_attribute(data_dict),
        url=parse_url_attribute(data_dict),
        post_code=parse_post_code_attribute(data_dict),
        location=parse_location_attribute(data_dict),
        rooms=parse_room_attribute(data_dict),
        floor=parse_floor_attribute(data_dict),
        address=parse_address_attribute(data_dict),
        image_urls=parse_image_urls_attribute(data_dict),
        coordinates=parse_coordinates_attribute(data_dict),
        free_area_type=parse_free_area_type_name_attribute(data_dict),
        free_area=parse_free_area_attribute(data_dict),
        advertiser=parser_advertiser_attribute(data_dict),
    )
