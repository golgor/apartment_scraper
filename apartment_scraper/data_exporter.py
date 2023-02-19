import csv
import json

from apartment_scraper import Apartment, Site, pkg_path


class DataExporter:
    def __init__(self, site: Site):
        self._clean_path = pkg_path.joinpath(site.value, "clean_data")
        self._raw_path = pkg_path.joinpath(site.value, "raw_data")

    def export_json(self, filename: str, apartments: list[Apartment]):
        path = pkg_path.joinpath("willhaben", "clean_data", filename)
        apartment_dict = {
            apartment.id: apartment.to_json() for apartment in apartments
        }
        with open(path, "w") as f:
            f.write(json.dumps(apartment_dict, indent=2))

    def export_excel(self, filename: str, apartments: list[Apartment]):
        # Example.csv gets created in the current working directory
        path = pkg_path.joinpath("willhaben", "clean_data", filename)
        with open(path, "w", newline="\n") as csvfile:
            my_writer = csv.writer(csvfile, delimiter=",")
            my_writer.writerow(apartments[0].columns)
            for apartment in apartments:
                my_writer.writerow(
                    (
                        apartment.area,
                        apartment.price,
                        apartment.url,
                        apartment.rooms,
                        apartment.post_code,
                        apartment.price_per_area,
                    )
                )
