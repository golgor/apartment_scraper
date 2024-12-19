from pydantic import BaseModel, Field


class ImmoweltPaging(BaseModel):
    size: int = 10
    page: int = 0


class ImmoweltRange(BaseModel):
    min: int | None = None
    max: int | None = None


class ImmoweltSortStrategy(BaseModel):
    direction: str = "DESC"
    field: str = "RELEVANCE"


class ImmoWeltBaseRequest(BaseModel):
    paging: ImmoweltPaging = Field(default_factory=ImmoweltPaging)
    primary_price: ImmoweltRange = Field(alias="primaryPrice", default_factory=ImmoweltRange)
    primary_area: ImmoweltRange = Field(alias="primaryArea", default_factory=ImmoweltRange)
    immo_item_types: list[str] = ["ESTATE", "PROJECT"]
    sort: ImmoweltSortStrategy


test = {
    "estateType": "APARTMENT",
    "distributionTypes": ["RENT", "LEASE"],
    # "estateSubtypes": [],
    "locationIds": [514061],
    # "featureFilters": [],
    # "excludedFeatureFilters": [],
    # "primaryPrice": {"min": None, "max": 1100},
    # "primaryArea": {"min": None, "max": None},
    "areas": [{"areaType": "PLOT_AREA", "min": None, "max": None}],
    "rooms": {"min": None, "max": None},
    "constructionYear": {"min": None, "max": None},
    "geoRadius": {"radius": None, "point": {"lat": None, "lon": None}},
    "zipCode": None,
    "sort": {"direction": "DESC", "field": "RELEVANCE"},
    # "immoItemTypes": ["ESTATE", "PROJECT"],
    # "paging": {"size": 8, "page": 0},
}
