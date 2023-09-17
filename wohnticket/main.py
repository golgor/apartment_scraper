from pathlib import Path
from typing import TYPE_CHECKING

from bs4 import BeautifulSoup
from selenium import webdriver


if TYPE_CHECKING:
    from bs4.element import ResultSet, Tag

URL = "https://wohnungssuche.wohnberatung-wien.at/?page=planungsprojekte-liste&p=3"

browser = webdriver.Chrome()
browser.get(URL)
soup = BeautifulSoup(browser.page_source, features="html.parser")

output = Path("output.html")
results: "ResultSet[Tag]" = soup.find_all("div", class_="media-wohnung", recursive=True)
