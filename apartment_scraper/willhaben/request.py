import asyncio
import itertools
from time import perf_counter
from typing import Any, Protocol

import httpx
from loguru import logger

from apartment_scraper.models import Apartment
from apartment_scraper.willhaben.parse import parse_apartment


class NoConnectionError(Exception):
    pass


class WillhabenRequest(Protocol):
    @property
    def url(self) -> str:  # noqa: ANN101
        """The url to get the data from.

        Returns:
            str: The url as a string.
        """
        ...

    @property
    def params(self) -> dict[str, str | int]:  # noqa: ANN101
        """Parameters to add to the request.

        Returns:
            dict[str, str | int]: _description_
        """
        ...

    @property
    def header(self) -> dict[str, str]:  # noqa: ANN101
        """Headers to add to the request.

        Returns:
            dict[str, str | int]: _description_
        """
        ...

    @property
    def rows(self) -> int:  # noqa: ANN101
        """The number of rows per request.

        A typical endpoint contains a lot of data and it is not feasible to get all data in one request.
        This is the number of rows per request, which in turns control how many requests have to be done
        for a specific endpoint.

        Returns:
            int: The number of rows per request.
        """
        ...

    @property
    def area_id(self) -> int:  # noqa: ANN101
        ...


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
