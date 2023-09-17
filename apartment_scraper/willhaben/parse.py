import json
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


def get_attribute_with_name(response: dict[str, Any], name: str) -> list[str]:
    """Get an attribute from a response dictionary.

    The dictionary with data about apartments is nested and contains a list of attributes. This function returns the
    specified attribute from the response dictionary.

    Args:
        response (dict[str, Any]): _description_
        name (str): _description_
        fallback (Any): _description_

    Returns:
        list[str] | Any: _description_
    """
    attributes: list[dict[str, Any]] = response["attributes"]["attribute"]
    return next(
        attribute["values"] for attribute in attributes if attribute["name"] == name
    )


def parse_price_attribute(response: dict[str, Any]) -> float:
    """Parses the 'PRICE' attribute from a response dictionary and returns it as a float.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        float: The parsed 'PRICE' attribute as a float.
    """
    try:
        price = float(get_attribute_with_name(response, "PRICE")[0])
    except Exception:
        logger.warning(f"Failed to parse the field 'PRICE' for id={response['id']}")
        return 0
    else:
        return price


def parse_url_attribute(response: dict[str, Any]) -> str:
    """Parses the 'SEO_URL' attribute from a response dictionary and returns it as a formatted URL string.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        str: The parsed 'SEO_URL' attribute as a formatted URL string.
    """
    try:
        if url := get_attribute_with_name(response, "SEO_URL")[0]:
            return f"https://www.willhaben.at/iad/{url}"
    except Exception:
        logger.warning(f"Failed to parse the field 'SEO_URL' for id={response['id']}")
        return ""
    else:
        return ""


def parser_advertiser_attribute(response: dict[str, Any]) -> str:
    """Parses the 'advertiserInfo' attribute from a response dictionary and returns its 'label' field as a string.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        str: The 'label' field of the 'advertiserInfo' attribute as a string.

    Raises:
        None.
    """
    try:
        advertiser = response["advertiserInfo"]["label"] or ""
    except Exception:
        logger.warning(f"Failed parse AdvertiserInfo for id={response['id']}")
        return ""
    else:
        return advertiser


def parse_post_code_attribute(response: dict[str, Any]) -> int:
    """Parses the 'POSTCODE' attribute from a response dictionary and returns it as a string.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        str: The parsed 'POSTCODE' attribute as a string.

    Raises:
        None.
    """
    try:
        postcode = int(get_attribute_with_name(response, "POSTCODE")[0])
    except Exception:
        logger.warning(f"Failed to parse the field 'POSTCODE' for id={response['id']}")
        return 0
    else:
        return postcode


def parse_id_attribute(response: dict[str, Any]) -> int:
    """Parses the 'ID' attribute from a response dictionary and returns it as a string.

    The 'ID' is a unique identifier for an apartment.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        str: The parsed 'ID' attribute as a string.
    """
    try:
        apartment_id = int(response["id"])
    except Exception:
        logger.warning(f"Failed to parse the field 'ID' for id={response['id']}")
        return 0
    else:
        return apartment_id


def parse_area_attribute(response: dict[str, Any]) -> int:
    """Parses the 'ESTATE_SIZE/LIVING_AREA' attribute from a response dictionary and returns it as a float.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        float: The parsed 'ESTATE_SIZE/LIVING_AREA' attribute as a float.

    Raises:
        None.
    """
    try:
        area = int(get_attribute_with_name(response, "ESTATE_SIZE/LIVING_AREA")[0])
    except Exception:
        logger.warning(
            f"Failed to parse the field 'ESTATE_SIZE/LIVING_AREA' for id={response['id']}"
        )
        return 0
    else:
        return area


def parse_room_attribute(response: dict[str, Any]) -> float:
    """Parses the 'NUMBER_OF_ROOMS' attribute from a response dictionary and returns it as a float.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        float: The parsed 'NUMBER_OF_ROOMS' attribute as a float.

    Raises:
        None.
    """
    try:
        area: float = float(get_attribute_with_name(response, "NUMBER_OF_ROOMS")[0])
    except Exception:
        logger.warning(
            f"Failed to parse the field 'NUMBER_OF_ROOMS' for id={response['id']}"
        )
        return 0
    else:
        return area


def parse_floor_attribute(response: dict[str, Any]) -> float:
    """Parses the 'FLOOR' attribute from a response dictionary and returns it as a float.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        float: The parsed 'FLOOR' attribute as a float.

    Raises:
        None.
    """
    try:
        floor: str = get_attribute_with_name(response, "FLOOR")[0]
        return float(floor)
    except Exception:
        logger.warning(f"Failed to parse the field 'FLOOR' for id={response['id']}")
        return 0


def parse_rent_attribute(response: dict[str, Any]) -> float:
    """Parses the 'RENT/PER_MONTH_LETTINGS' attribute from a response dictionary and returns it as a float.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        float: The parsed 'RENT/PER_MONTH_LETTINGS' attribute as a float.

    Raises:
        None.
    """
    try:
        rent: str = get_attribute_with_name(response, "RENT/PER_MONTH_LETTINGS")[0]
        return round(float(rent), 2)
    except Exception:
        logger.warning(f"Failed to parse the field 'RENT' for id={response['id']}")
        return 0


def parse_address_attribute(response: dict[str, Any]) -> str:
    """Parses the 'ADDRESS' attribute from a response dictionary and returns it as a string.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        str: The parsed 'ADDRESS' attribute as a string.

    Raises:
        None.
    """
    try:
        address: str = get_attribute_with_name(response, "ADDRESS")[0]
    except Exception:
        logger.warning(f"Failed to parse the field 'ADDRESS' for id={response['id']}")
        return ""
    return address


def parse_free_area_attribute(response: dict[str, Any]) -> int:
    """Parses the 'FREE_AREA/FREE_AREA_AREA_TOTAL' attribute from a response dictionary and returns it as an integer.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        int: The parsed 'FREE_AREA/FREE_AREA_AREA_TOTAL' attribute as an integer.

    Raises:
        None.
    """
    try:
        free_area: list[str] = get_attribute_with_name(
            response, "FREE_AREA/FREE_AREA_AREA_TOTAL"
        )
        return int(free_area[0])
    except Exception:
        logger.warning(f"Failed to parse the field 'FREE_AREA' for id={response['id']}")
        return 0


def parse_free_area_type_name_attribute(response: dict[str, Any]) -> str:
    """Parses the 'FREE_AREA_TYPE_NAME' attribute from a response dictionary and returns it as a list of strings.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        list[str]: The parsed 'FREE_AREA_TYPE_NAME' attribute as a list of strings.

    Raises:
        None.
    """
    try:
        free_area_type: list[str] = get_attribute_with_name(
            response, "FREE_AREA_TYPE_NAME"
        )
    except Exception:
        logger.warning(
            "Failed to parse the field 'FREE_AREA_TYPE_NAME' for "
            f"id={response['id']}"
        )
        return json.dumps([])
    return json.dumps(free_area_type)


def parse_status_attribute(response: dict[str, Any]) -> bool:
    """Parses the 'advertStatus' attribute from a response dictionary and returns the status.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        bool: True if the 'id' field of the 'advertStatus' attribute is 'active', False otherwise.
    """
    active: str = response["advertStatus"]["id"]
    return active == "active"


def parse_image_urls_attribute(response: dict[str, Any]) -> str:
    """Parses the 'ALL_IMAGE_URLS' attribute from a response dictionary and returns a list of formatted URL strings.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        list[str]: The parsed 'ALL_IMAGE_URLS' attribute as a list of formatted URL strings.

    Raises:
        None.
    """
    # sourcery skip: use-named-expression
    try:
        urls: str = get_attribute_with_name(response, "ALL_IMAGE_URLS")[0]
        if urls:
            return json.dumps([f"https://cache.willhaben.at/mmo/{url}" for url in urls.split(";")])
        else:
            return json.dumps([])
    except Exception:
        logger.warning(
            f"Failed to parse the field 'ALL_IMAGE_URLS' for id={response['id']}"
        )
        return json.dumps([])


def parse_coordinates_attribute(response: dict[str, Any]) -> str:
    """Parses the 'COORDINATES' attribute from a response dictionary and returns it as a string.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        str: The parsed 'COORDINATES' attribute as a string.

    Raises:
        None.
    """
    try:
        coordinates: str = get_attribute_with_name(response, "COORDINATES")[0]
    except Exception:
        logger.warning(
            f"Failed to parse the field 'COORDINATES' for id={response['id']}"
        )
        return ""
    return coordinates


def parse_product_id_attribute(response: dict[str, Any]) -> str:
    """Parses the 'PRODUCT_ID' attribute from a response dictionary and returns it as a string.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        str: The parsed 'PRODUCT_ID' attribute as a string.

    Raises:
        None.
    """
    try:
        product_id: str = get_attribute_with_name(response, "PRODUCT_ID")[0]
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
            f"Failed to parse the field 'PRODUCT_ID' for id={response['id']}"
        )
        return ""


def parse_location_attribute(response: dict[str, Any]) -> str:
    """Parses the 'LOCATION' attribute from a response dictionary and returns it as a string.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        str: The parsed 'LOCATION' attribute as a string.

    Raises:
        None.
    """
    try:
        location: str = get_attribute_with_name(response, "LOCATION")[0]
    except Exception:
        logger.warning(f"Failed to parse the field 'LOCATION' for id={response['id']}")
        return ""
    else:
        return location


def parse_property_type_attribute(response: dict[str, Any]) -> str:
    """Parses the 'PROPERTY_TYPE' attribute from a response dictionary and returns it as a string.

    Args:
        response (dict[str, Any]): The response dictionary to parse.

    Returns:
        str: The parsed 'PROPERTY_TYPE' attribute as a string.

    Raises:
        None.
    """
    try:
        property_type: str = get_attribute_with_name(response, "PROPERTY_TYPE")[0]
    except Exception:
        logger.warning(
            f"Failed to parse the field 'PROPERTY_TYPE' for id={response['id']}"
        )
        return ""
    else:
        return property_type


def calc_rent_per_area(response: dict[str, Any]) -> float:
    """Calculates the rent per area of a response dictionary and returns it as a float.

    Args:
        response (dict[str, Any]): The response dictionary to calculate.

    Returns:
        float: The calculated rent per area as a float.

    Raises:
        None.
    """
    try:
        rent = parse_rent_attribute(response)
        area = parse_area_attribute(response)
        rent_per_area = round(float(rent) / float(area), 2)
    except Exception:
        logger.warning(f"Failed to calculate rent/area for id={response['id']}")
        return 0
    else:
        return rent_per_area


def calc_price_per_area(response: dict[str, Any]) -> float:
    """Calculates the price per area of a response dictionary and returns it as a float.

    Args:
        response (dict[str, Any]): The response dictionary to calculate.

    Returns:
        float: The calculated price per area as a float.

    Raises:
        None.
    """
    try:
        rent = parse_price_attribute(response)
        area = parse_area_attribute(response)
        price_per_area = round(float(rent) / float(area), 2)
    except Exception:
        logger.warning(f"Failed to calculate price/area for id={response['id']}")
        return 0
    else:
        return price_per_area


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
        prio=0,
    )
