import json
from datetime import datetime
from enum import Enum

from apartment_scraper import Apartment, Site, immowelt, pkg_path, willhaben
from apartment_scraper.data_exporter import DataExporter
from apartment_scraper.data_loader import DataLoader


def get_willhaben_raw_data(area_id: Enum):
    wh = willhaben.Haus(area_id=area_id)
    raw_data = willhaben.get_data(wh)

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
    areas = [
        willhaben.AreaId.NIEDERÖSTERREICH.KORNEUBURG,
        willhaben.AreaId.NIEDERÖSTERREICH.TULLN,
        willhaben.AreaId.NIEDERÖSTERREICH.GÄNSERNDORF,
        willhaben.AreaId.NIEDERÖSTERREICH.MISTELBACH,
        willhaben.AreaId.NIEDERÖSTERREICH.MÖLDLING,
        willhaben.AreaId.NIEDERÖSTERREICH.KREMS_AN_DER_DONAU,
        willhaben.AreaId.NIEDERÖSTERREICH.KREMS_LAND,
        willhaben.AreaId.NIEDERÖSTERREICH.SANKT_PÖLTEN,
        willhaben.AreaId.NIEDERÖSTERREICH.SANKT_PÖLTEN_LAND,
        willhaben.AreaId.NIEDERÖSTERREICH.BADEN,
        willhaben.AreaId.NIEDERÖSTERREICH.WIENER_NEUSTADT,
        willhaben.AreaId.NIEDERÖSTERREICH.HOLLABRUNN,
    ]
    for area in areas:
        get_willhaben_raw_data(area_id=area)
    # parse_raw_data(today, site=Site.WILLHABEN)
