from apartment_scraper import pkg_path, willhaben
from apartment_scraper.models import Model

if __name__ == "__main__":
    model = Model(path=pkg_path.joinpath("test.db"))

    areas = [
        willhaben.AreaId.NIEDERÖSTERREICH.KORNEUBURG,
        # willhaben.AreaId.NIEDERÖSTERREICH.TULLN,
        # willhaben.AreaId.NIEDERÖSTERREICH.GÄNSERNDORF,
        # willhaben.AreaId.NIEDERÖSTERREICH.MISTELBACH,
        # willhaben.AreaId.NIEDERÖSTERREICH.MÖDLING,
        # willhaben.AreaId.NIEDERÖSTERREICH.KREMS_AN_DER_DONAU,
        # willhaben.AreaId.NIEDERÖSTERREICH.KREMS_LAND,
        # willhaben.AreaId.NIEDERÖSTERREICH.SANKT_PÖLTEN,
        # willhaben.AreaId.NIEDERÖSTERREICH.SANKT_PÖLTEN_LAND,
        # willhaben.AreaId.NIEDERÖSTERREICH.BADEN,
        # willhaben.AreaId.NIEDERÖSTERREICH.WIENER_NEUSTADT_LAND,
        # willhaben.AreaId.NIEDERÖSTERREICH.WIENER_NEUSTADT,
        # willhaben.AreaId.NIEDERÖSTERREICH.HOLLABRUNN,
    ]

    for area in areas:
        wh = willhaben.KaufWohnungen(area_id=area)
        raw_data = willhaben.get_data(wh)
        apartments = willhaben.parse_willhaben_response(elements=raw_data)
        model.add_apartments(apartments)
