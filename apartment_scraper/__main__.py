import scraper


URL = "https://www.immowelt.at/liste/wien/wohnungen/mieten"


def main():
    scraper.scrape_immowelt(URL)


if __name__ == "__main__":
    main()
