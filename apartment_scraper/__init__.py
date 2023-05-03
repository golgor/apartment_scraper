import pathlib
from enum import StrEnum

__version__ = "0.0.1b"

# Creating a variable for the system path to the 'pbt'-directory
pkg_path = pathlib.Path(__file__).parent.resolve()


class Site(StrEnum):
    WILLHABEN = "willhaben"
    IMMOWELT = "immowelt"
