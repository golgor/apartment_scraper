from apartment_scraper import pkg_path, willhaben
from apartment_scraper.models import Model

if __name__ == "__main__":
    model = Model(path=pkg_path.joinpath("test.db"))
    # area = willhaben.AreaId.WIEN.LIESING
    # wh = willhaben.MietWohnungen(area_id=area)
    # raw_data = willhaben.get_data(wh)
    # apartments = willhaben.parse_willhaben_rent_response(elements=raw_data)
    # model.add_apartments(apartments)
    model.dump_to_csv(filename="dump.csv")
