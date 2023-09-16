from pathlib import Path
from bs4 import BeautifulSoup
from typing import TYPE_CHECKING
from selenium import webdriver

if TYPE_CHECKING:
    from bs4.element import Tag, ResultSet

URL = "https://wohnungssuche.wohnberatung-wien.at/?page=planungsprojekte-liste&p=3"

browser = webdriver.Chrome()
browser.get(URL)
soup = BeautifulSoup(browser.page_source, features="html.parser")

output = Path("output.html")
results: "ResultSet[Tag]" = soup.find_all(
    "div", class_="media-wohnung", recursive=True
)

for element in results[:1]:
    print(element)
