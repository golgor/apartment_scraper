from typing import Any, Protocol
import httpx
from apartment_scraper import willhaben
import asyncio
from time import perf_counter
import itertools
from apartment_scraper.models import Apartment
from apartment_scraper.willhaben.parse import parse_apartment


class NoConnectionError(Exception):
    pass


class WillhabenRequest(Protocol):
    @property
    def url(self) -> str:
        ...

    @property
    def params(self) -> dict[str, str | int]:
        ...

    @property
    def header(self) -> dict[str, str]:
        ...

    @property
    def rows(self) -> int:
        ...

    @property
    def page(self) -> int:
        ...

    @page.setter
    def page(self, value: int):
        ...

    @property
    def area_id(self) -> int:
        ...


async def get_apartments(
    client: httpx.AsyncClient,
    url: str,
    params: dict[str, Any],
    header: dict[str, Any],
) -> list[Apartment]:
    """Async function to get apartments from willhaben.at

    _extended_summary_

    Args:
        client (httpx.AsyncClient): An async httpx client
        url (str): A url to get the data from
        params (dict[str, Any]): Any parameters to pass to the request
        header (dict[str, Any]): Any headers to pass to the request

    Returns:
        list[Apartment]: A list of Apartment objects
    """
    response = await client.get(url=url, params=params, headers=header)

    raw_data: dict[str, Any] = response.json()
    apartment_data: list[dict[str, Any]] = raw_data["advertSummaryList"][
        "advertSummary"
    ]
    return [parse_apartment(data) for data in apartment_data]


async def get_data(obj: WillhabenRequest) -> list[Apartment]:
    number_of_rows_per_request = 5
    headers = {
        "x-wh-client": "api@willhaben.at;responsive_web;server;1.0.0;desktop",
        "accept": "application/json",
    }

    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get(
            "https://www.willhaben.at/webapi/iad/search/atz/seo/immobilien/mietwohnungen/wien/wien-1230-liesing",
            params={"rows": 1, "page": 1},
            headers=headers,
            timeout=60,
        )
        rows_found = response.json()["rowsFound"]

        required_pages = rows_found // number_of_rows_per_request
        if rows_found % number_of_rows_per_request != 0:
            required_pages += 1

        tasks: list[asyncio.Task[Any]] = []
        start_time = perf_counter()
        tasks.extend(
            asyncio.create_task(
                get_apartments(
                    client=client,
                    url="https://www.willhaben.at/webapi/iad/search/atz/seo/immobilien/mietwohnungen/wien/wien-1230-liesing",
                    params={
                        "rows": number_of_rows_per_request,
                        "page": page,
                    },
                    header=headers,
                )
            )
            for page in range(1, 5)
        )
        data: list[list[Apartment]] = await asyncio.gather(*tasks)
        print(f"Time with tasks: {perf_counter() - start_time}")
        return list(itertools.chain(*data))


if __name__ == "__main__":
    area = willhaben.AreaId.WIEN.LIESING
    wh = willhaben.MietWohnungen(area_id=area)
    test = asyncio.run(willhaben.get_data(wh))
    print(test[0].address)
    print(type(test[0]))
