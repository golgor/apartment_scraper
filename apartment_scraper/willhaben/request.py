import asyncio
import itertools
from dataclasses import dataclass
from enum import Enum
from time import perf_counter
from typing import Any, Self

import httpx
from loguru import logger

from apartment_scraper.models import Apartment
from apartment_scraper.willhaben.parse import parse_apartment


class NoConnectionError(Exception):
    pass


@dataclass
class Request:
    """A class to generate urls for willhaben.at.

    As the URL depends on the area_id choosen, the actual urls are generated depending on on the input.
    """

    area_id: Enum

    @property
    def miet_wohnung_url(self: Self) -> str:
        """The generated url for rental apartments in the specified area."""
        return f"https://www.willhaben.at/webapi/iad/search/atz/seo/immobilien/mietwohnungen/{self.area_id.value}"

    @property
    def kauf_wohnung_url(self: Self) -> str:
        """The generated url for apartments to buy in the specified area."""
        return f"https://www.willhaben.at/webapi/iad/search/atz/seo/immobilien/eigentumswohnung/{self.area_id.value}"

    @property
    def miet_haus_url(self: Self) -> str:
        """The generated url for rental houses in the specified area."""
        return f"https://www.willhaben.at/webapi/iad/search/atz/seo/immobilien/haus-mieten/{self.area_id.value}"

    @property
    def kauf_haus_url(self: Self) -> str:
        """The generated url for rental houses in the specified area."""
        return f"https://www.willhaben.at/webapi/iad/search/atz/seo/immobilien/haus-kaufen/{self.area_id.value}"


async def get_apartments(
    client: httpx.AsyncClient,
    url: str,
    params: dict[str, Any],
    header: dict[str, Any],
) -> list[Apartment]:
    """Async function to get apartments from willhaben.at.

    _extended_summary_

    Args:
        client (httpx.AsyncClient): An async httpx client
        url (str): A url to get the data from
        params (dict[str, Any]): Any parameters to pass to the request
        header (dict[str, Any]): Any headers to pass to the request

    Returns:
        list[Apartment]: A list of Apartment objects
    """
    logger.info(f"Page: {params['page']}")
    response = await client.get(url=url, params=params, headers=header)

    raw_data: dict[str, Any] = response.json()
    apartment_data: list[dict[str, Any]] = raw_data["advertSummaryList"][
        "advertSummary"
    ]
    return [parse_apartment(data) for data in apartment_data]


async def get_data(url: str, rows_per_request: int = 200) -> list[Apartment]:
    """Get apartments from willhaben.at.

    The function will first get the number of rows found for the specified endpoint. It is using 1 row and 1 page to
    minimize the number of data to be transferred. Then it will calculate the number of pages needed to get all the
    data. It is adding 1 if the result is not even, as for example 710 needs 8 pages, not 7.

    After that it will create a list of tasks to get the data from the specified endpoint, one for each page. The tasks
    will be executed with asyncio.gather all data.

    Each task  will return a list of Apartment objects, which means that the result of asyncio.gather will be a list of
    lists of Apartment objects. To flatten the list of lists, itertools.chain is used.

    Args:
        url (str): A url to an endpoint where to get the data from.
        rows_per_request (int, optional): The number of rows per request. Defaults to 200.

    Raises:
        ValueError: If not rows are found for the current endpoint.

    Returns:
        list[Apartment]: A list of Apartment objects.
    """
    header = {
        "accept": "application/json",
        "x-wh-client": ("api@willhaben.at;responsive_web;server;1.0.0;desktop"),
    }

    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(
            url,
            params={"rows": 1, "page": 1},
            headers=header,
            timeout=60,
        )
        response_json: dict[str, Any] = response.json()
        rows_found = response_json.get("rowsFound")
        logger.info(f"Rows found: {rows_found}")
        if not rows_found:
            raise ValueError("No rows found")

        required_pages = rows_found // rows_per_request
        if rows_found % rows_per_request != 0:
            required_pages += 1

        tasks: list[asyncio.Task[Any]] = []
        start_time = perf_counter()
        tasks.extend(
            asyncio.create_task(
                get_apartments(
                    client=client,
                    url=url,
                    params={
                        "rows": rows_per_request,
                        "page": page,
                    },
                    header=header,
                )
            )
            for page in range(1, required_pages + 1)
        )
        data: list[list[Apartment]] = await asyncio.gather(*tasks)
        logger.info(f"Time with tasks: {perf_counter() - start_time}")
        return list(itertools.chain(*data))
