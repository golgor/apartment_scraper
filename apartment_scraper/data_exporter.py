import csv
import json

from apartment_scraper import Apartment, Site, pkg_path


class DataExporter:
    def __init__(self, site: Site):
        self.site = site
        self._clean_path = pkg_path.joinpath(site.value, "clean_data")
        self._raw_path = pkg_path.joinpath(site.value, "raw_data")

    def export_json(self, filename: str, apartments: list[Apartment]):
        """Export the data to a .JSON file.

        It is structured as a dict containing information about each element.
        The key is the id, which is assumed to be unique.

        Args:
            filename (str): The filename to save the data to.
            apartments (list[Apartment]): A data source to dump.
        """
        path = pkg_path.joinpath(self.site.value, "clean_data", filename)
        apartment_dict = {
            apartment.id: apartment.to_dict() for apartment in apartments
        }
        with open(path, "w") as f:
            f.write(json.dumps(apartment_dict, indent=2))

    def export_excel(self, filename: str, apartments: list[Apartment]):
        """Export the data to a .csv file.

        Args:
            filename (str): The filename to save the data to.
            apartments (list[Apartment]): A data source to dump.
        """
        path = pkg_path.joinpath(self.site.value, "clean_data", filename)
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
                        apartment.floor,
                        apartment.post_code,
                        apartment.price_per_area,
                    )
                )
