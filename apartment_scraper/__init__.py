import pathlib
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Iterable

__version__ = "0.0.1b"

# Creating a variable for the system path to the 'pbt'-directory
pkg_path = pathlib.Path(__file__).parent.resolve()


class Site(StrEnum):
    WILLHABEN = "willhaben"
    IMMOWELT = "immowelt"
