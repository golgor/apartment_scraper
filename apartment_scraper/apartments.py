import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import logging


# Logging: https://docs.python.org/3/howto/logging-cookbook.html

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler("apartments.log")
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)-12s - %(name)-12s -  %(levelname)-8s %(message)s\n', datefmt='%m-%d %H:%M')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

FILE = "apartments.txt"

# TODO: Implement class method to validate URL, see:
# https://stackoverflow.com/questions/25200763/how-to-return-none-if-constructor-arguments-invalid


class Apartment:
    def __init__(self, url: str):
        self.url = url

    def get_source(self):
        r = requests.get(self.url)
        self._soup = BeautifulSoup(r.content, features="html.parser")

        # If the current url is not available anymore, a message is given
        # in a div. I.e. if this div is on the page, the object is no
        # longer available on the site. Setting internal values to None
        # makes all other values to default to N/A.
        # TODO: Remove this instance from the apartmentlist
        if self._soup.find("div", "message_info understitial_message_box"):
            self._quick_facts = None
            self._hardfacts = None
            return -1

        self._quick_facts = self._soup.find("div", "quickfacts iw_left")
        self._hardfacts = self._soup.find("div", "hardfacts clear")

    def get_location(self):
        if self._quick_facts:
            location_div = self._quick_facts.find("span", "no_s")
            location = location_div.text.split()

            self.bezirk_no = parse_bezirk_no(location)
            self.city = parse_city(location)
            self.bezirk_name = parse_bezirk_name(location)
            self.address = parse_address(location)
        else:
            self.city = "N/A"
            self.bezirk_no = "N/A"
            self.bezirk_name = "N/A"
            self.address = "N/A"

    def get_title(self):
        try:
            self._title = self._quick_facts_div.h1.text
        except Exception:
            self._title = "N/A"

    def get_hard_facts(self):
        if self._hardfacts:
            hardfacts = re.sub("[\s.]", "", str(self._hardfacts).lower())
            self.rent = get_value_with_regex(div=hardfacts, regex="[0-9,]+€")
            self.area = get_value_with_regex(div=hardfacts, regex="([0-9,]+)m")
            self.rooms = get_value_with_regex(div=hardfacts, regex=">([0-9])<")
        else:
            logger.error(f"No hard facts div found for object {self.url}")
            self.rent = "N/A"
            self.area = "N/A"
            self.rooms = "N/A"

    def __str__(self) -> str:
        return (
            f"Link: {self.url}\n"
            f"City: {self._city}\n"
            f"Bezirk: {self.bezirk_no}. {self.bezirk_name}\n"
            f"Address: {self.address}\n"
            f"Rent: {self.rent}\n"
            f"Area: {self.area}\n"
            f"Rooms: {self.rooms}\n"
        )


def get_value_with_regex(div: str, regex: str) -> str:
    try:
        # Try to find the regex as provided and return
        # the value, else return N/A
        value = re.search(regex, div).group()

        # Only return numeric values, i.e. strip any €, m² and similar.
        return re.sub("[^0-9,]", "", value)
    except AttributeError as e:
        # This error will occur if no expression is found. re.search
        # will return None which does not have the attribute 'group'
        logger.info(f"{e} - No substring found")
        return "N/A"
    except Exception as e:
        logger.error(f"{e} ({regex}) in:\n{div}\n")
        return "N/A"


def get_parsed(source: BeautifulSoup, name: str, tag_type="div") -> str:
    div = source.find(tag_type, name)
    return re.sub("[\s.]", "", str(div).lower())


def parse_bezirk_no(quick_fact_list: list) -> int:
    try:
        if quick_fact_list[0].isnumeric():
            return int(quick_fact_list[0][1:3])
    except Exception:
        return 0


def parse_city(quick_fact_list: list) -> str:
    return quick_fact_list[1]


def parse_bezirk_name(quick_fact_list: list) -> str:
    try:
        return re.sub("[^A-Za-z]", "", quick_fact_list[2])
    except Exception:
        logger.info(f"{quick_fact_list} - No bezirk name found")
        return ""


def parse_address(quick_fact_list: list) -> str:
    try:
        return quick_fact_list[3]
    except Exception:
        return ""


with open(FILE) as f:
    apartment_list = [
        Apartment(apartment)
        for apartment
        in f.read().split("\n")[:-1]
    ]

data = pd.DataFrame(columns=["rent", "area", "rooms", "bezirk_no",
                             "bezirk_name", "city", "url"])


for idx, apartment in enumerate(apartment_list):
    print(f"Processing id: {idx}")
    apartment.get_source()
    apartment.get_hard_facts()
    apartment.get_location()
    data.loc[idx] = (
        apartment.rent,
        apartment.area,
        apartment.rooms,
        # apartment.address,
        apartment.bezirk_no,
        apartment.bezirk_name,
        apartment.city,
        apartment.url
    )

data.to_excel("apartments.xlsx")
