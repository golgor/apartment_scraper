from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING, Any, Self


@dataclass
class WillHabenRequest:
    """A class to generate urls for willhaben.at.

    As the URL depends on the area_id choosen, the actual urls are generated depending on on the input.
    """

    area_id: Enum

    @property
    def mietwohnung_url(self: Self) -> str:
        """The generated url for rental apartments in the specified area."""
        return f"https://www.willhaben.at/webapi/iad/search/atz/seo/immobilien/mietwohnungen/{self.area_id.value}"

    @property
    def kaufwohnung_url(self: Self) -> str:
        """The generated url for apartments to buy in the specified area."""
        return f"https://www.willhaben.at/webapi/iad/search/atz/seo/immobilien/eigentumswohnung/{self.area_id.value}"
