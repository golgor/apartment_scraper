import json
from datetime import datetime

from apartment_scraper import Apartment, Site, immowelt, pkg_path, willhaben
from apartment_scraper.data_exporter import DataExporter
from apartment_scraper.data_loader import DataLoader


def get_willhaben_raw_data(obj: willhaben.Wohnungen | willhaben.Haus):
    raw_data = willhaben.get_data(obj)

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{wh.name}_{today}"

    filepath = pkg_path.joinpath("willhaben", "raw_data", f"{filename}.json")
    with open(filepath, "w") as f:
        f.write(json.dumps(raw_data, indent=2))
        print(f"Successfully saved {len(raw_data)}")


def get_immowelt_raw_data(filename: str):
    access_token = immowelt.get_immowelt_token()
    request = immowelt.WohnungenWien(access_token)

    test = immowelt.get_data(request)

    filepath = pkg_path.joinpath("immowelt", "raw_data", f"{filename}.json")
    with open(filepath, "w") as f:
        f.write(json.dumps(test, indent=2))
        print(f"Successfully saved {len(test)}")


def parse_raw_data(filename: str, site: Site) -> list[Apartment]:
    dl = DataLoader(site=site)

    raw_data = dl.load_raw_data(filename)

    if site == Site.IMMOWELT:
        apartments = immowelt.parse_immowelt_response(raw_data)
    elif site == Site.WILLHABEN:
        apartments = willhaben.parse_willhaben_response(raw_data)
    else:
        raise ValueError("No valid site selected!")
    return apartments


if __name__ == "__main__":
    de = DataExporter(site=Site.WILLHABEN)
    # de.export_json(filename, apartments)
    # de.export_csv(filename, apartments)
    areas = [
        willhaben.AreaId.WIEN.DONAUSTADT,
    ]

    for area in areas:
        wh = willhaben.Wohnungen(area_id=area)
        get_willhaben_raw_data(wh)

    # raw_data_path = pkg_path.joinpath("willhaben", "raw_data")
    # paths = raw_data_path.glob("wohnungen_wien*.json")
    # apartments: list[Apartment] = []
    # for path in paths:
    #     parsed_path = str(path).split(".")[0]
    #     apartments.extend(parse_raw_data(parsed_path, Site.WILLHABEN))
    # print(len(apartments))
    # de.export_csv("Wohnungen", apartments)
