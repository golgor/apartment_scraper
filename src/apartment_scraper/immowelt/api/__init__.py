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

    WIEN = 514061
    MEIDLING = 516384
    LIESING = 516394
    PENZING = 514061
    ALSERGRUND = 516381


if __name__ == "__main__":
    body = ImmoweltRentalApartmentRequestBody(location_ids=[LocationIds.LIESING])
    asyncio.run(get_rental_apartments(body))


# When searching for Liesing, the follow ids were used: locationIds":[532729,526560,526770,516394,514061,513966,513957]
# The id for Liesing is 516394, the others might be Vienna, Austria, etc?
# It also reported "lowestLevelLocationId":516394
# This was found out when searching on the web app. It was using the URL https://www.immowelt.at/suche/wien-23-liesing/immobilien/mk
