import json
from datetime import datetime

import willhaben

from apartment_scraper import Site, pkg_path
from apartment_scraper.data_exporter import DataExporter
from apartment_scraper.data_loader import DataLoader


def get_willhaben_raw_data(filename: str):
    wh = willhaben.WohnungenWien()
    test = willhaben.get_data(wh)

    filepath = pkg_path.joinpath("willhaben", "raw_data", filename)
    with open(filepath, "w") as f:
        f.write(json.dumps(test, indent=2))
        print(f"Successfully saved {len(test)}")


def parse_willhaben_raw_data(filename: str):
    dl = DataLoader(site=Site.WILLHABEN)
    de = DataExporter(site=Site.WILLHABEN)
    raw_data = dl.load_raw_data(filename)
    apartments = willhaben.parse_willhaben_response(raw_data)
    de.export_json(filename, apartments)


if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"willhaben_{today}.json"
    # get_willhaben_raw_data(filename)
    parse_willhaben_raw_data(filename)
