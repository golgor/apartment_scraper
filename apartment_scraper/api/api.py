import schemas
from fastapi import FastAPI, HTTPException

from apartment_scraper import pkg_path
from apartment_scraper.models import Apartment, Model

app = FastAPI()
model = Model(path=pkg_path.joinpath("test.db"))


@app.get(
    "/apartments",
    response_model=dict[str, int | list[schemas.ApartmentSchema]],
)
def rent(
    pagesize: int = 100, page: int = 0
) -> dict[str, int | list[Apartment]]:
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
