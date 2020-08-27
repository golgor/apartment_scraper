import logging
import re
from time import perf_counter
import concurrent.futures

import pandas as pd
import requests
from bs4 import BeautifulSoup

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

# TODO: Implement class method to validate URL, see:
# https://stackoverflow.com/questions/25200763/how-to-return-none-if-constructor-arguments-invalid


def get_source(apartment) -> BeautifulSoup:
    """Function to getting the source from a url.

    Args:
        apartment (Apartment): The object to process.

    Returns:
        BeautifulSoup: Soup of the source.
    """
    try:
        r = requests.get(apartment.url)
        # Todo, check for http-status?
        print(f"Fetching source: {apartment.url}")
        return r.content
    except requests.exceptions.ConnectionError:
        logger.error("Connection refused by target server.")
    except Exception as e:
        logger.error(f"Couldn't not find source {e}"
                     f"soup for object {apartment.url}.")
        return None


def get_div(soup, html_type, class_name: str):
    """Function to scrape the two facts divs from a soup.

    Args:
        soup (Beautifulsoup): A soup where to find a pattern.
        regex (str): A regex string to use.

    Returns:
        soup: If found, returns a soup for the div with the wanted class.
    """
    try:
        div = soup.find(html_type, class_name)
        if div:
            return div
        else:
            logger.info(f"No tag with type '{html_type}' and "
                        f"attribute '{class_name}' found!")
            return None
    except Exception:
        logger.error(f"No soup found to parse for a '{html_type}' "
                     f"with attribute '{class_name}'")
        return None


def get_value_with_regex(div: str, regex: str) -> str:
    """Get a value from a str that matches a specific regex.

    Args:
        div (str): A stringified div to search.
        regex (str): A regex expression.

    Returns:
        str: A value matching the pattern from the regex.
    """
    if div is None:
        return None
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
        return None
    except Exception as e:
        logger.error(f"{e} ({regex}) in:\n{div}\n")
        return None


def stringify_div(div):
    if div is not None:
        return re.sub("[\s.]", "", str(div).lower())
    else:
        return None


def get_location(div):
    if div is None:
        return None, None
    location_list = div.text.split()
    return location_list[0][1:3], location_list[1]


class Apartment:
    def __init__(self, url: str):
        self.url = url
        # If the current url is not available anymore, a message is given
        # in a div. I.e. if this div is on the page, the object is no
        # longer available on the site. Setting internal values to None
        # makes all other values to default to N/A.
        # TODO: Remove this instance from the apartmentlist

    def fetch_data(self):
        """Function to fetch the data and specific divs

        Typically 0.3 - 0.4 seconds (IO Bound)
        """
        self.source = get_source(self)

    def parse_data(self):
        """Function to parse the data using Beautifulsoups HTML-parser
        and finding specific divs.

        Typical time consumption: 0.36-0.4 seconds (CPU bound)
        """
        try:
            self.soup = BeautifulSoup(self.source, features="html.parser")
        except Exception:
            self.soup = None

        self.quickfacts = get_div(self.soup, "div", "quickfacts iw_left")
        self.hardfacts = get_div(self.soup, "div", "hardfacts clear")

    def process_data(self):
        """Processing the soups and finding specific expressions using regex.

        Note: Timing is excluding the parse_data() call at the start
        of the function.
        Typical time consumption: 200-300µs (CPU Bound)
        """
        self.parse_data()

        hardfacts = stringify_div(self.hardfacts)
        self.rent = get_value_with_regex(div=hardfacts, regex="[0-9,]+€")
        self.area = get_value_with_regex(div=hardfacts, regex="([0-9,]+)m")
        self.rooms = get_value_with_regex(div=hardfacts, regex=">([0-9])<")

        quickfacts = get_div(self.quickfacts, "span", "no_s")
        self.bezirk, self.city = get_location(quickfacts)


def fetch(apartment):
    apartment.fetch_data()


def process(apartment):
    apartment.process_data()
    return (apartment.rent, apartment.area, apartment.rooms,
            apartment.bezirk, apartment.city)


# ~264s with threading  with 10 workers without ProcessPool
# ~268s with threading with 15 workers without ProcessPool
# ~143 with threading with 2 workers with ProcessPool with 16 workers
def main(file):
    start = perf_counter()
    with open(file) as f:
        apartment_list = [
            Apartment(apartment)
            for apartment
            in f.read().split("\n")[:-1]
        ]

    data = pd.DataFrame(
        columns=["rent", "area", "rooms", "bezirk_no", "city", "url"]
    )

    print("Started fetching".center(50, "="))
    start_io = perf_counter()
    # Using threading with IO Bound fetching of data.
    # High amount of workers lead to that Connections are refused.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(fetch, apartment_list)
    print(f"Done fetching data in: {perf_counter() - start_io}")

    # with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    #     executor.map(process, apartment_list[:15])

    print("Started processing".center(50, "="))
    start_process = perf_counter()
    with concurrent.futures.ProcessPoolExecutor(max_workers=16) as executor:
        results = executor.map(process, apartment_list)
    print(f"Time for processing: {perf_counter() - start_process}")

    start_save = perf_counter()
    for result, apartment in zip(results, apartment_list):
        apartment.rent = result[0]
        apartment.area = result[1]
        apartment.rooms = result[2]
        apartment.bezirk = result[3]
        apartment.city = result[4]

    for idx, apartment in enumerate(apartment_list):
        data.loc[idx] = (
            apartment.rent,
            apartment.area,
            apartment.rooms,
            apartment.bezirk,
            apartment.city,
            apartment.url
        )

    print(f"Time for saving data: {perf_counter() - start_save}")
    data.to_excel("apartments.xlsx")
    print(f"Time with threading: {perf_counter() - start}")


FILE = "apartments.txt"
if __name__ == "__main__":
    main(FILE)
