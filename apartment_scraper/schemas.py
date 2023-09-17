import datetime

from pydantic import BaseModel


class ApartmentSchema(BaseModel):
    id: int
    apartment_id: int
    status: bool
    product_id: str
    area: int
    url: str
    rooms: float
    floor: int
    address: str
    post_code: str
    location: str
    coordinates: str | None
    price: float | None
    price_per_area: float | None
    free_area_type: list[str] | None
    free_area: int | None
    image_urls: list[str] | None
    advertiser: str
    prio: int | None
    updated: datetime.datetime | None
    created: datetime.datetime

    class Config:
        from_attributes = True
