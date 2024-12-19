from pydantic import BaseModel, Field


class ImmoweltPaging(BaseModel):
    """Model for the paging parameters."""

    size: int = 10
    page: int = 0


class ImmoweltRange(BaseModel):
    """Model for the range parameters."""

    min: int | None = None
    max: int | None = None


class ImmoweltSortStrategy(BaseModel):
    """Model for the sort parameters."""

    direction: str = "DESC"
    field: str = "RELEVANCE"


class ImmoweltLocation(BaseModel):
    """Model for the location parameters."""

    lat: float | None = None
    lon: float | None = None


class ImmoweltRadius(BaseModel):
    """Model for the radius parameters.

    This is a location and a radius from that location.
    """

    radius: int | None = None
    point: ImmoweltLocation


class ImmoWeltBaseRequest(BaseModel):
    """A BaseModel for a request containing all the parameters that is similar for all requests."""

    location_ids: list[int] = Field(serialization_alias="locationIds")
    primary_price: ImmoweltRange = Field(serialization_alias="primaryPrice", default_factory=ImmoweltRange)
    primary_area: ImmoweltRange = Field(serialization_alias="primaryArea", default_factory=ImmoweltRange)
    rooms: ImmoweltRange = Field(default_factory=ImmoweltRange)
    construction_year: ImmoweltRange = Field(serialization_alias="constructionYear", default_factory=ImmoweltRange)
    zip_code: int | None = None
    sort: ImmoweltSortStrategy = Field(default_factory=ImmoweltSortStrategy)
    immo_item_types: list[str] = ["ESTATE", "PROJECT"]
    paging: ImmoweltPaging = Field(default_factory=ImmoweltPaging)


class ImmoweltRentalApartmentRequestBody(ImmoWeltBaseRequest):
    """The body of the request."""

    estate_type: str = Field(default="APARTMENT", alias="estateType")
    distribution_types: list[str] = Field(default=["RENT", "LEASE"], alias="distributionTypes")


mega = ImmoweltRentalApartmentRequestBody(location_ids=[514061])
print(mega.model_dump_json(indent=4, by_alias=True))

test = {
    # "estateType": "APARTMENT",
    # "distributionTypes": ["RENT", "LEASE"],
    # "estateSubtypes": [],
    # "locationIds": [514061],
    # "featureFilters": [],
    # "excludedFeatureFilters": [],
    # "primaryPrice": {"min": None, "max": 1100},
    # "primaryArea": {"min": None, "max": None},
    "areas": [{"areaType": "PLOT_AREA", "min": None, "max": None}],
    # "rooms": {"min": None, "max": None},
    # "constructionYear": {"min": None, "max": None},
    # "geoRadius": {"radius": None, "point": {"lat": None, "lon": None}},
    # "zipCode": None,
    # "sort": {"direction": "DESC", "field": "RELEVANCE"},
    # "immoItemTypes": ["ESTATE", "PROJECT"],
    # "paging": {"size": 8, "page": 0},
}
