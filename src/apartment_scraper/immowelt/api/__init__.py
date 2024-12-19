import asyncio
import os
from enum import IntEnum
from typing import Any

import httpx
from dotenv import load_dotenv
from result import Err, as_async_result

from apartment_scraper.immowelt.api.exceptions import NoTokenFoundError
from apartment_scraper.immowelt.api.immowelt_token import with_token
from apartment_scraper.immowelt.api.immowelt_types import ImmoweltRentalApartmentRequestBody


load_dotenv(override=True)


@as_async_result(Exception)
@with_token
async def perform_query(request: httpx.Request) -> dict[str, Any]:
    token = os.getenv("IMMOWELT_RESIDENTIAL_SEARCH_TOKEN")
    if not token:
        raise NoTokenFoundError()

    request.headers["Authorization"] = f"Bearer {token}"

    async with httpx.AsyncClient() as client:
        response = await client.send(request)
    return response.json()


async def get_rental_apartments(body: ImmoweltRentalApartmentRequestBody) -> list[dict[str, Any]]:
    url = "https://api.immowelt.com/residentialsearch/v1/searches"
    request = httpx.Request("POST", url, json=body.model_dump(by_alias=True))
    response = await perform_query(request)

    if isinstance(response, Err):
        raise response.err()

    return response.ok_value


class LocationIds(IntEnum):
    """A enumeration for the different locations in the immowelt api."""

    WIEN_STADT = 514061
    WIEN_STATE = 513966
    ÖSTERREICH = 513957
    MEIDLING = 516384
    LIESING = 516394
    PENZING = 516386
    ALSERGRUND = 516381
    BRIGITTENAU = 516391
    OTTAKRING = 516388
    RUDOLFSHEIM = 516387
    SIMMERING = 516383
    WIEDEN = 516375
    WÄHRING = 516390
    NEUBAU = 516379
    MARIAHILF = 516378
    MARGARETEN = 516377
    LEOPOLDSTADT = 516188
    LANDSTRASSE = 516374
    JOSEFSTADT = 516380
    INNERE_STADT = 516367
    HIETZING = 516385
    HERNALS = 516389
    FLORIDSDORF = 516392
    FAVORITEN = 516382
    DÖBLING = 516189
    DONAUSTADT = 516393


if __name__ == "__main__":
    body = ImmoweltRentalApartmentRequestBody(location_ids=[LocationIds.LIESING])
    asyncio.run(get_rental_apartments(body))


# When searching for Liesing, the follow ids were used: locationIds":[532729,526560,526770,516394,514061,513966,513957]
# The id for Liesing is 516394, the others might be Vienna, Austria, etc?
# It also reported "lowestLevelLocationId":516394
# This was found out when searching on the web app. It was using the URL https://www.immowelt.at/suche/wien-23-liesing/immobilien/mk
