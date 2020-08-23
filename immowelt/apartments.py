from numpy.lib.function_base import append
import requests
import re
from time import perf_counter
from bs4 import BeautifulSoup
import pandas as pd
import logging


logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
f_handler = logging.FileHandler('file.log')
c_handler.setLevel(logging.WARNING)
f_handler.setLevel(logging.ERROR)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
c_handler.setFormatter(c_format)
f_handler.setFormatter(f_format)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)

FILE = "apartments.txt"

class Apartment:
    def __init__(self, url: str):
        # self._url = "https://www.immowelt.at/expose/2vges4g"
        self._url = url
    
    def get_source(self):
        r = requests.get(self._url)
        self._soup = BeautifulSoup(r.content, features="html.parser")
        self._quick_facts_div = self._soup.find("div", "quickfacts iw_left")
        self._hardfacts_div = self._soup.find("div", "hardfacts clear")

    def get_location(self):
        try:
            location_div = self._quick_facts_div.find("div", "location")
            location = location_div.span.text.split()

            self._city = location[1]
            self._bezirk_no = location[2].strip("().,")
            self._bezirk_name = location[3].strip("().,")
            self._street_adress = location[4] if len(location) == 5 else None

        except:
            self._city = "N/A"
            self._bezirk_no = "N/A"
            self._bezirk_name = "N/A"
            self._street_adress = "N/A"
            logger.error("Error i Location!")

    def get_title(self):
        try:
            self._title = self._quick_facts_div.h1.text
        except:
            self._title = "No title"
            logger.error("Error i title!")

    def get_facts(self):
        self.get_title()
        self.get_location()
        test = re.findall("[0-9,.]+ ", str(self._hardfacts_div))
        try:
            self._rent = test[0]
            self._area = test[1]
            self._rooms = test[2]
        except:
            self._rent = 1
            self._area = 1
            self._rooms = 1
            logger.error("Error i facts")

    def __str__(self) -> str:
        return (
            f"Link: {self._url}\n"
            f"City: {self._city}\n"
            f"Bezirk: {self._bezirk_no}. {self._bezirk_name}\n"
            f"Address: {self._street_adress}\n"
            f"Rent: {self._rent}\n"
            f"Area: {self._area}\n"
            f"Rooms: {self._rooms}\n"
        )

with open(FILE) as f:
    apartment_list = [Apartment(apartment) for apartment in f.read().split("\n")[:-1]]

data = pd.DataFrame(columns=["Hyra","Yta", "Url"])


for idx, apartment in enumerate(apartment_list):
    print(f"Processing id: {idx}")
    apartment.get_source()
    apartment.get_facts()
    data.loc[idx] = (apartment._rent, apartment._area, apartment._url)

data.to_excel("test.xlsx")