from datetime import datetime
from typing import Any, Optional

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from apartment_scraper import pkg_path
from apartment_scraper.models import ApartmentRent, Model

app = FastAPI()
model = Model(path=pkg_path.joinpath("test.db"))


class ApartmentRentSchema(BaseModel):
    apartment_id: int
    area: int
    rent: int

    class Config:
        orm_mode = True


@app.get("/", response_model=list[ApartmentRentSchema])
def index() -> list[ApartmentRent]:
    return model.get_rentals()
