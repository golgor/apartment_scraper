import datetime

from pydantic import BaseModel


class ApartmentSchema(BaseModel):
    """Schema for the Apartment model."""
    id: int  # noqa: A003
    apartment_id: int
    status: bool
    product_id: str
    property_type: str
    area: int
    url: str
    rooms: float
    floor: float
    address: str
    post_code: int
    location: str
    coordinates: str | None
    price: float
    price_per_area: float | None
    free_area_type: str | None
    free_area: int | None
    image_urls: str | None
    advertiser: str
    prio: int
    updated: datetime.datetime | None

    class Config:
        """Schema configuration."""
        from_attributes = True
