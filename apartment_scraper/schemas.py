import datetime
from typing import Optional

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
    coordinates: Optional[str]
    price: Optional[float]
    price_per_area: Optional[float]
    free_area_type: Optional[list[str]]
    free_area: Optional[int]
    image_urls: Optional[list[str]]
    advertiser: str
    prio: Optional[int]
    updated: Optional[datetime.datetime]
    created: datetime.datetime

    class Config:
        from_attributes = True
