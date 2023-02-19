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
            "post_code",
            "price_per_area",
        ]

    def to_json(self):
        return {
            "area": self.area,
            "price": self.price,
            "url": self.url,
            "rooms": self.rooms,
            "floor": self.floor,
            "post_code": self.post_code,
        }
