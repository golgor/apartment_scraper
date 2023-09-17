from fastapi import FastAPI, HTTPException
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import PlainTextResponse

from apartment_scraper import pkg_path, schemas
from apartment_scraper.models import Apartment, Model


app = FastAPI()
model = Model(path=pkg_path.joinpath("test.db"))


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request, exc: ResponseValidationError):
    errors = exc.errors()
    for error in errors:
        print(f"Parameter location: {error['loc']}")
        print(f"Debug message: {error['msg']}")
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/", response_model=dict[str, str])
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


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
    result = model.update_apartment_prio(apartment_id=apartment_id, prio=prio)
    if result is None:
        raise HTTPException(
            status_code=404, detail=f"Apartment {apartment_id} not found"
        )
    return {"updated": result}
