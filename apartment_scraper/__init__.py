import pathlib
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Iterable

__version__ = "0.0.1b"

# Creating a variable for the system path to the 'pbt'-directory
pkg_path = pathlib.Path(__file__).parent.resolve()


class Site(StrEnum):
    WILLHABEN = "willhaben"


@dataclass
class Apartment:
    id: str
    area: float
    price: float
    url: str = field(repr=False)
    # coordinates: tuple[float, float]
    rooms: int
    floor: int
    # address: str
    # broker: str = ""
    post_code: str

    @property
    def price_per_area(self):
        try:
            return round(self.price / self.area, 0)
        except Exception:
            print("Division by zero")
            return 0

    @property
    def columns(self) -> Iterable[str]:
        return [
            "id",
            "area",
            "price",
            "url",
            "rooms",
            "floor",
            "post_code",
            "price_per_area",
        ]

    def to_dict(self):
        return {
            "area": self.area,
            "price": self.price,
            "url": self.url,
            "rooms": self.rooms,
            "floor": self.floor,
            "post_code": self.post_code,
            "price_per_area": self.price_per_area,
        }


class PostCodeWien(StrEnum):
    UNDEFINED = "0"
    INNERE_STADT = "1010"
    LEOPOLDSTADT = "1020"
    LANDSTRASSE = "1030"
    WIEDEN = "1040"
    MARGARETEN = "1050"
    MARIAHILF = "1060"
    NEUBAU = "1070"
    JOSEFSTADT = "1080"
    ALSERGRUND = "1090"
    FAVORITEN = "1100"
    SIMMERING = "1110"
    MEIDLING = "1120"
    HIETZING = "1130"
    PENZING = "1140"
    RUDOLFSHEIM_FUNFHAUS = "1150"
    OTTAKRING = "1160"
    HERNALS = "1170"
    WÄHRING = "1180"
    DÖBLING = "1190"
    BRIGITTENAU = "1200"
    FLORIDSDORF = "1210"
    DONAUSTADT = "1220"
    LIESING = "1230"
