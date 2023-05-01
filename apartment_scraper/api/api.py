from typing import Any

import schemas
from fastapi import FastAPI, HTTPException

from apartment_scraper import pkg_path
from apartment_scraper.models import ApartmentBuy, ApartmentRent, Model

app = FastAPI()
model = Model(path=pkg_path.joinpath("test.db"))


@app.get(
    "/rent", response_model=dict[str, int | list[schemas.ApartmentRentSchema]]
)
def rent(
    pagesize: int = 100, page: int = 0
) -> dict[str, int | list[ApartmentRent]]:
    if pagesize > 500:
        raise HTTPException(
            status_code=413, detail="Pagesize cannot be greater than 500"
        )
    data, elements, count = model.get_rentals(page=page, pagesize=pagesize)
    return {
        "pagesize": pagesize,
        "page": page,
        "fetched_elements": elements,
        "total_elements": count,
        "data": data,
    }


@app.get("/buy", response_model=list[schemas.ApartmentBuySchema])
def buy() -> list[ApartmentBuy]:
    return model.get_freiwohnungen()
