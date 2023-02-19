import json
from typing import Any

from apartment_scraper import Apartment, Site, pkg_path


class DataLoader:
    def __init__(self, site: Site):
        self.clean_path = pkg_path.joinpath(site.value, "clean_data")
        self.raw_path = pkg_path.joinpath(site.value, "raw_data")

    def load_clean_data(self, filename: str) -> list[Apartment]:
        filepath = self.clean_path.joinpath(filename)
        with open(filepath, "r") as f:
            data: dict[str, Any] = json.load(f)

        return [
            Apartment(id=id, **apartment_data)
            for id, apartment_data in data.items()
        ]
