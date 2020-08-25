import time
import re
from collections import Counter
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--incognito")

URL = "https://www.immowelt.at/liste/wien-10-favoriten/wohnungen/mieten"
# URL = "https://www.immowelt.at/liste/wien/wohnungen/mieten"
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', chrome_options=chrome_options)


def close_webdriver():
    driver.quit()


def get_source():
    page_source = driver.page_source
    return BeautifulSoup(page_source, 'html.parser')


def set_driver_url(url):
    driver.get(url)


def get_apartments(url: str, expected_results: int, counter):
    listings = 0
    max_tries = 10
    current_tries = 0
    apartment_divs = []

    # Set the URL to scrape
    set_driver_url(url)

    while listings < expected_results:
        # Scroll to bottom of the page, forcing the
        # page to add more apartment entries.
        # Then get the source of the page.
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(0.3)
        source = get_source()
        time.sleep(0.3)

        # Find all divs for apartments and count how many.
        # Need regex due to different premium and regular divs.
        regex = re.compile('listitem.*relative js-listitem')
        apartment_divs = set(source.findAll("div", regex))
        listings = len(apartment_divs)

        # Sleep for a short while to give some time for
        # the pages javascript to run
        time.sleep(0.4)

        # To avoid infinite loop in case expected hits are to high.
        if current_tries >= max_tries:
            break
        current_tries += 1

    # Can be used to debug, printing out the soup.
    # with open(f"{counter}.txt", "w") as file:
    #     file.write(str(source))

    return apartment_divs


def find_number_of_pages(source):
    """Takes in the source from Immowelt and finds how many pages with
    listings exists. Does this by finding the label of a button that
    goes to the last page. Button is located at the buttom of the page.

    Args:
        source (BeautifulSoup): The html source of the page.

    Returns:
        int: The number of pages with listings.
    """
    # Row with buttons to navigate to different pages. Numeric labels.
    buttons = source.findAll("a", "btn_01 white")

    # Get the last button, indicating the last page
    last_button = buttons[-1]

    # Get the label value from the button
    last_page = int(last_button['href'].split("=")[-1])

    return last_page


def generate_listing_urls(url: str, max_count: int):
    urls = [
        "?".join([url, f"cp={count}"])
        for count
        in range(2, max_count + 1)
    ]
    return [url] + urls


def get_apartments_urls(apartments):
    return [
        "https://www.immowelt.at" + apartment.find("a")['href']
        for apartment
        in apartments
    ]


def collect_apartment_urls(url):
    set_driver_url(url)
    source = get_source()
    listing_urls = []

    number_of_pages = find_number_of_pages(source)
    # print(f"Number of pages: {number_of_pages}")

    # Generate all pages where apartments objects are.
    page_urls = generate_listing_urls(url, number_of_pages)

    # Scrape all the pages and append apartment URLs.
    for idx, page_url in enumerate(page_urls, 1):
        print(f"Scraping page {idx}/{number_of_pages}")
        apartments = get_apartments(page_url, 20, idx)
        test_urls = get_apartments_urls(apartments)
        for url in test_urls:
            print(url)
        listing_urls += test_urls

        print(f"Total apartment links found: {len(listing_urls)}")

    set_of_apartments = set(listing_urls)

    with open("apartments.txt", "w") as file:
        for url in set_of_apartments:
            file.write(url + "\n")


collect_apartment_urls(URL)

close_webdriver()
