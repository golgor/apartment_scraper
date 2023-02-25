import json
from datetime import datetime

from apartment_scraper import Site, immowelt, pkg_path, willhaben
from apartment_scraper.data_exporter import DataExporter
from apartment_scraper.data_loader import DataLoader


def get_willhaben_raw_data(filename: str):
    wh = willhaben.WohnungenWien()
    test = willhaben.get_data(wh)

    filepath = pkg_path.joinpath("willhaben", "raw_data", f"{filename}.json")
    with open(filepath, "w") as f:
        f.write(json.dumps(test, indent=2))
        print(f"Successfully saved {len(test)}")



def parse_raw_data(filename: str, site: Site):
    dl = DataLoader(site=site)
    de = DataExporter(site=site)
    raw_data = dl.load_raw_data(filename)

    if site == Site.IMMOWELT:
        apartments = immowelt.parse_immowelt_response(raw_data)
    elif site == Site.WILLHABEN:
        apartments = willhaben.parse_willhaben_response(raw_data)
    else:
        raise ValueError("No valid site selected!")

    de.export_json(filename, apartments)
    de.export_csv(filename, apartments)


if __name__ == "__main__":
    today = datetime.now().strftime("%Y-%m-%d")
    # filename = "2023-02-24_test"
    # get_willhaben_raw_data(today)
    parse_raw_data(today, site=Site.WILLHABEN)
