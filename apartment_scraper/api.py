from typing import TYPE_CHECKING

from fastapi import FastAPI, HTTPException, Response
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import PlainTextResponse
from loguru import logger

from apartment_scraper import schemas
from apartment_scraper.models import Apartment, Model


if TYPE_CHECKING:
    from starlette.requests import Request

MAX_PAGE_SIZE = 500  # max number of apartments to return per page

app = FastAPI()
model = Model()


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(
    request: "Request", exc: ResponseValidationError
) -> PlainTextResponse:
    """Function to response to validation errors.

    This is primarily used to log the errors during development. It returns a plain text what the problem is, instead
    of just a 500 error or a crash.

    Args:
        request (Request): A request object.
        exc (ResponseValidationError): An error object.

    Returns:
        PlainTextResponse: A plain text response with the reason for the error.
    """
    errors = exc.errors()
    for error in errors:
        logger.error(f"Parameter location: {error['loc']}")
        logger.error(f"Debug message: {error['msg']}")
    return PlainTextResponse(str(exc), status_code=400)


@app.get("/", response_model=dict[str, str])
def read_root() -> dict[str, str]:
    """Returns a dictionary with a single key-value pair.

    Typically only used to test connectivity.

    Returns:
        dict[str, str]: A dictionary with a single key "Hello" and value "World".

    Raises:
        None
    """
    return {"Hello": "World"}


@app.get(
    "/apartments/",
    response_model=dict[str, int | list[schemas.ApartmentSchema]],
)
def query_all_apartments( # noqa: PLR0913
    pagesize: int = 100,
    page: int = 0,
    min_area: int = 0,
    min_room: int = 0,
    max_price: int = 0,
    min_price: int = 0,
    exclude_property_types: str | None = None,
) -> dict[str, int | list[Apartment]]:
    """Endpoint to get all apartments from the database.

    Using pagination to limit the number of apartments returned per page.

    Args:
        pagesize (int, optional): The page size. Defaults to 100.
        page (int, optional): What page to return. Defaults to 0.
        min_area (int, optional): _description_. Defaults to 0.
        min_room (int, optional): _description_. Defaults to 0.
        max_price (int, optional): _description_. Defaults to 0.
        min_price (int, optional): _description_. Defaults to 0.
        exclude_property_types (str | None, optional): _description_. Defaults to None.

    Raises:
        HTTPException: In case of demanding a page size greater than 500.

    Returns:
        dict[str, int | list[Apartment]]: Returns a list of data regarding the query as well as the data itself.
    """
    if pagesize > MAX_PAGE_SIZE:
        raise HTTPException(
            status_code=413, detail="Pagesize cannot be greater than 500"
        )
    if exclude_property_types is not None:
        exclude_property_types = exclude_property_types.replace(" ", "")
        exclude_property_types_parsed = list(exclude_property_types.split(","))
    else:
        exclude_property_types_parsed = None

    data, elements, count = model.get_paged_apartments(
        page=page,
        pagesize=pagesize,
        min_area=min_area,
        min_room=min_room,
        max_price=max_price,
        min_price=min_price,
        exclude_property_types=exclude_property_types_parsed,
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
    """Retrieves an apartment by its ID.

    Args:
        apartment_id (int): The ID of the apartment.

    Returns:
        Apartment: The apartment object.

    Raises:
        HTTPException: Raised when the apartment with the given ID is not found.
    """
    apartment = model.get_apartment_by_id(apartment_id)
    if apartment is None:
        raise HTTPException(
            status_code=404, detail=f"Apartment {apartment_id} not found"
        )
    return apartment


@app.put("/apartments/{apartment_id}")
def update_prio_of_apartment(
    apartment_id: int,
    prio: int,
) -> Response:
    """Function to update the priority of an apartment."""
    if not model.update_apartment_prio(apartment_id=apartment_id, prio=prio):
        raise HTTPException(
            status_code=404, detail=f"Apartment {apartment_id} not found"
        )
    return Response(status_code=204)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # noqa: S104 - This is the main entrypoint only for development.
