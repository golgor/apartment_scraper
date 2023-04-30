from pydantic import BaseModel


class ApartmentRentSchema(BaseModel):
    apartment_id: int
    area: int
    rent: int

    class Config:
        orm_mode = True


class ApartmentBuySchema(BaseModel):
    apartment_id: int
    area: int
    price: int

    class Config:
        orm_mode = True
