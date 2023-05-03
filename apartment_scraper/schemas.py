from typing import Optional

from pydantic import BaseModel


class ApartmentSchema(BaseModel):
    id: int
    apartment_id: int
    area: int
    price: int
    price_per_area: float
    url: str
    rooms: float
    floor: int
    address: str
    post_code: str
    location: str
    coordinates: Optional[str]
    free_area_type: Optional[list[str]]
    free_area: Optional[int]
    image_urls: Optional[list[str]]
    advertiser: str
    prio: Optional[int]
    product_id: str

    class Config:
        orm_mode = True
