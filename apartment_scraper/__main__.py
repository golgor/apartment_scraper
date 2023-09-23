import asyncio

import folium
from dotenv import load_dotenv

from apartment_scraper import pkg_path, willhaben
from apartment_scraper.models import Model


# Loads the environment variables from .env file
load_dotenv()

def main() -> None:
    """Main function of the application."""
    model = Model()
    areas = [willhaben.AreaId.WIEN.ALL]

    for area in areas:
        wh = willhaben.Request(area_id=area)
        apartments = asyncio.run(willhaben.get_data(url=wh.kauf_haus_url))
        model.add_apartments(apartments)


def get_color(price_per_area: int) -> str:
    cheap = 2_000
    average = 3_500
    expensive = 5_000

    if price_per_area < cheap:
        return "green"
    elif price_per_area < average:
        return "yellow"
    elif price_per_area < expensive:
        return "orange"
    else:
        return "red"


def get_free_area(free_area: int) -> str:
    no_area = 0
    small_area = 50
    big_area = 200

    if free_area == no_area:
        return "red"
    elif free_area < small_area:
        return "orange"
    elif free_area < big_area:
        return "yellow"
    else:
        return "green"


def get_rooms_color(rooms: int) -> str:
    small_apartment = 3
    average_apartment = 4
    big_apartment = 5

    if rooms < small_apartment:
        return "red"
    elif rooms < average_apartment:
        return "orange"
    elif rooms < big_apartment:
        return "yellow"
    else:
        return "green"


def get_price_color(price: int) -> str:
    cheap_apartment = 250_000
    average_apartment = 300_000
    expensive_apartment = 350_000

    if price < cheap_apartment:
        return "green"
    elif price < average_apartment:
        return "yellow"
    elif price < expensive_apartment:
        return "orange"
    else:
        return "red"


def create_map() -> None:
    """Create a map with all apartments in the database."""
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
                f"Price: {apartment.price}<br>Area: {apartment.area}<br>Rooms: {apartment.rooms}<br>"
                "Price/m2: {apartment.price_per_area}<br>Free area: {apartment.free_area}"
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
    create_map()
    # main()
