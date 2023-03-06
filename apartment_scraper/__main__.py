from apartment_scraper import pkg_path, willhaben
from apartment_scraper.models import Model

if __name__ == "__main__":
    model = Model(path=pkg_path.joinpath("test.db"))
    area = willhaben.AreaId.WIEN.ALL
    wh = willhaben.Wohnungen(area_id=area)
    raw_data = willhaben.get_data(wh)
    apartments = willhaben.parse_willhaben_response(
        elements=raw_data, type="kaufen"
    )
    model.add_apartments(apartments)
