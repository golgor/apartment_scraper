from enum import StrEnum


class EstateType(StrEnum):
    """Estate types for immowelt.at."""
    house="HOUSE"
    premises="PREMISES"
    shop_area="SHOPAREA"
    commerce_premises="COMMERCE_PREMISES"
    garage_parking_space="GARAGE_PARKING_SPACE"
    income_property="INCOME_PROPERTY"
    halls_industrial_area="HALLS_INDUSTRIAL_AREA"
    other="OTHER"
    apartment= "APARTMENT"
    temporary_living="TEMPORARY_LIVING"
    shared_apartment="SHARED_APARTMENT"
    gastronomy_hotels="GASTRONOMY_HOTELS"
    office_practice_area="OFFICE_PRACTICE_AREA"
    agriculture_forestry="AGRICULTURE_FORESTRY"

class DistributionTypes(StrEnum):
    """Distribution types for immowelt.at."""
    sale="SALE"
    rent="RENT"
    lease="LEASE"
    rentsale="RENTSALE"
