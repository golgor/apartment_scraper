import time
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def initialize_webdriver():
    """Initialize an instance of a Chrome Webdriver.

    Returns:
        Webdriver: An instance of a Webdriver.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")

    return webdriver.Chrome(
        executable_path='/usr/bin/chromedriver',
        options=chrome_options
    )


def set_driver_url(driver, url: str):
    """Sets the url to the Chrome driver.

    Args:
        driver (Webdriver): An instance of a Webdriver.
        url (str): The url to the site to be scraped.
    """
    driver.get(url)


def close_webdriver(driver):
    """Closes the Chrome driver.

    Args:
        driver (Webdriver): An instance of a Webdriver.
    """
    driver.quit()


def get_source(driver):
    """Downloads the source of the page and returns a soup instance.

    Returns:
        Beautifulsoup: A soup instance of the page source.
    """
    page_source = driver.page_source
    return BeautifulSoup(page_source, 'html.parser')


def generate_listing_urls(url: str, max_count: int):
    """Generate urls for all the pages, based on the number of pages.

    Creating urls such as:
    * https://www.immowelt.at/liste/wien-10-favoriten/wohnungen/mieten?cp=2
    * https://www.immowelt.at/liste/wien-10-favoriten/wohnungen/mieten?cp=3

    Where "?cp=x" is the page number, and
    "https://www.immowelt.at/liste/wien-10-favoriten/wohnungen/mieten" is the
    base-url.

    Args:
        url (str): Base-url to append to.
        max_count (int): How many pages/urls that should be generated.

    Returns:
        list: A list with all the urls following url syntax for Immowelt.
    """
    urls = [
        "?".join([url, f"cp={count}"])
        for count
        in range(2, max_count + 1)
    ]
    return [url] + urls


def get_list_source(driver):
    """Immowelt are using scripting to delay the page from loading.
    While scrolling down, more items are loaded, thus we have to emulate
    scrolling down to load all the listed objects on the page.

    This function are using javascript to scroll down to the bottom of the
    page and then wait 0.3 second, and then tries to scroll down to the bottom
    again. It does this 5 times, and it is assumed the whole listings page is
    generated at that time.

    Args:
        driver (Webdriver): An instance of a Webdriver.

    Returns:
        Beautifulsoup: Returns an instance of Beautifulsoup containing
        the full source.
    """
    for _ in range(5):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )
        time.sleep(0.3)
    return get_source(driver)


def get_apartment_divs(driver):
    """Scrapes the url the driver is pointing at and extract
    any divs with "listitems". Those divs are used as
    apartment objects at Immowelt.

    Args:
        driver (Webdriver): A Webdriver instance.

    Returns:
        list: returns a list of all divs of class listitem...
    """
    source = get_list_source(driver)
    regex = re.compile('listitem.*relative js-listitem')
    return set(source.findAll("div", regex))


def scrape_apartment_urls(driver, page_url):
    """Function that scrapes the current listing page for urls
    to individual apartment pages.

    Using get_apartment_divs() to get the divs from the linsting page,
    then use Beautifulsoup to parse for the 'a'-tag.

    Args:
        driver (Webdriver): An instance of a Webdriver.
        page_url (str): The url to the listings page.

    Returns:
        list: A list with urls to indiviual apartments.
    """
    set_driver_url(driver, page_url)
    apartments = get_apartment_divs(driver)

    return [
        "https://www.immowelt.at" + apartment.find("a")['href']
        for apartment
        in apartments
    ]


def scrape_page_count(source):
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


def get_number_of_pages(url):
    """Function that will scrape for the number of pages
    with listed apartments available. This number will
    then be used to generate urls that will be scraped
    for individual apartments.

    Args:
        url (str): Url to first page of listings.

    Returns:
        int: The number of pages that contains listed apartments.
    """
    driver = initialize_webdriver()
    set_driver_url(driver, url)
    source = get_source(driver)
    close_webdriver(driver)

    return scrape_page_count(source)


def save_to_file(urls):
    with open("apartments.txt", "w") as file:
        for url in urls:
            file.write(url + "\n")


def scrape_immowelt(url):
    number_of_pages = get_number_of_pages(url)

    # Generate all pages where apartments objects are.
    page_urls = generate_listing_urls(url, number_of_pages)

    driver = initialize_webdriver()

    urls = []
    for idx, page_url in enumerate(page_urls, 1):
        print(f"Scraping page {idx}/{len(page_urls)}")
        apartment_urls = scrape_apartment_urls(driver, page_url)
        urls += apartment_urls

    # Close the driver
    close_webdriver(driver)

    print(f"Total apartment links found: {len(urls)}")
    save_to_file(urls)
