import asyncio

import folium

from apartment_scraper import pkg_path, willhaben
from apartment_scraper.models import Model
from apartment_scraper.willhaben.wohnungen import WillHabenRequest


def main() -> None:
    """Main function of the application."""
    model = Model(path=pkg_path.joinpath("test.db"))
    areas = [willhaben.AreaId.WIEN.BRIGITTENAU]

    for area in areas:
        wh = WillHabenRequest(area_id=area)
        apartments = asyncio.run(willhaben.get_data(url=wh.kaufwohnung_url))
        model.add_apartments(apartments)


def get_color(price_per_area: int) -> str:
    if price_per_area < 2000:
        return "green"
    elif price_per_area < 3500:
        return "yellow"
    elif price_per_area < 5000:
        return "orange"
    else:
        return "red"


def get_free_area(free_area: int) -> str:
    if free_area == 0:
        return "red"
    elif free_area < 50:
        return "orange"
    elif free_area < 200:
        return "yellow"
    else:
        return "green"


def get_rooms_color(rooms: int) -> str:
    if rooms < 3:
        return "red"
    elif rooms < 4:
        return "orange"
    elif rooms < 5:
        return "yellow"
    else:
        return "green"


def get_price_color(price: int) -> str:
    if price < 250000:
        return "green"
    elif price < 300000:
        return "yellow"
    elif price < 350000:
        return "orange"
    else:
        return "red"


def map() -> None:
    base_map = folium.Map(location=[48.20849, 16.37208], zoom_start=11)

    folium.GeoJson("bezirke_95_geo.json").add_to(base_map)

    model = Model(path=pkg_path.joinpath("test.db"))
    apartments = model.get_map_data()

    for apartment in apartments:
        if not apartment.coordinates:
            continue
        folium.Circle(
            location=apartment.coordinates.split(","),
            tooltip=(
                f"Price: {apartment.price}<br>Area: {apartment.area}<br>Rooms: {apartment.rooms}<br>Price/m2: {apartment.price_per_area}<br>Free area: {apartment.free_area}"
            ),
            popup=f"<a href='{apartment.url}'>{apartment.apartment_id}</a>",
            color=get_rooms_color(apartment.rooms),
            radius=100,
            fill=True,
            fillOpacity=0.4,
            fillColor=get_price_color(apartment.price),
        ).add_to(base_map)

    base_map.show_in_browser()


if __name__ == "__main__":
    # map()
    main()
