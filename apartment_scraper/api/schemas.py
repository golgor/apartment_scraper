from typing import Optional

from pydantic import BaseModel


class ApartmentRentSchema(BaseModel):
    id: int
    apartment_id: int
    area: int
    rent: int
    url: str
    rooms: float
    floor: int
    address: str
    post_code: str
    coordinates: Optional[str]
    free_area_type: Optional[str]
    free_area: Optional[int]
    image_urls: Optional[list[str]]
    apartment_type: str

    class Config:
        orm_mode = True


class ApartmentBuySchema(BaseModel):
    apartment_id: int
    area: int
    price: int
    url: str
    rooms: float
    floor: int
    address: str
    post_code: str
    coordinates: Optional[str]
    free_area_type: Optional[str]
    free_area: Optional[int]
    image_urls: Optional[list[str]]
    apartment_type: str

    class Config:
        orm_mode = True
