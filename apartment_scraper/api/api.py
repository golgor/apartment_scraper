import schemas
from fastapi import FastAPI, HTTPException

from apartment_scraper import pkg_path
from apartment_scraper.models import Apartment, Model

app = FastAPI()
model = Model(path=pkg_path.joinpath("test.db"))


@app.get(
    "/apartments/",
    response_model=dict[str, int | list[schemas.ApartmentSchema]],
)
def query_all_apartments(
    pagesize: int = 100, page: int = 0
) -> dict[str, int | list[Apartment]]:
    if pagesize > 500:
        raise HTTPException(
            status_code=413, detail="Pagesize cannot be greater than 500"
        )
    data, elements, count = model.get_paged_apartments(
        page=page, pagesize=pagesize
    )
    return {
        "pagesize": pagesize,
        "page": page,
        "fetched_elements": elements,
        "total_elements": count,
        "data": data,
    }


@app.get(
    "/apartments/{apartment_id}",
    response_model=schemas.ApartmentSchema,
)
def query_apartment_by_id(apartment_id: int) -> Apartment:
    apartment = model.get_apartment_by_id(apartment_id)
    if apartment is None:
        raise HTTPException(
            status_code=404, detail=f"Apartment {apartment_id} not found"
        )
    return apartment


@app.put(
    "/apartments/{apartment_id}",
    response_model=dict[str, schemas.ApartmentSchema],
)
def add_apartment(
    apartment_id: int,
    prio: int,
) -> dict[str, Apartment]:
    apartment = model.get_apartment_by_id(apartment_id)
    if apartment is None:
        raise HTTPException(
            status_code=404, detail=f"Apartment {apartment_id} not found"
        )
    model.update_apartment_prio(apartment_id=apartment_id, prio=prio)
    apartment = model.get_apartment_by_id(apartment_id)
    if apartment is None:
        raise HTTPException(
            status_code=404, detail=f"Apartment {apartment_id} not found"
        )
    return {"updated": apartment}
