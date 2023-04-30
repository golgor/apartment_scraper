import schemas
from fastapi import FastAPI

from apartment_scraper import pkg_path
from apartment_scraper.models import ApartmentBuy, ApartmentRent, Model

app = FastAPI()
model = Model(path=pkg_path.joinpath("test.db"))


@app.get("/rent", response_model=list[schemas.ApartmentRentSchema])
def rent() -> list[ApartmentRent]:
    return model.get_rentals()


@app.get("/buy", response_model=list[schemas.ApartmentBuySchema])
def buy() -> list[ApartmentBuy]:
    return model.get_freiwohnungen()
