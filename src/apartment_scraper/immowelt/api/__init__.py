import os
from typing import Any

import httpx
from dotenv import load_dotenv
from result import as_async_result

from apartment_scraper.immowelt.api.exceptions import NoTokenFoundError
from apartment_scraper.immowelt.api.immowelt_token import get_token


load_dotenv()


@as_async_result(Exception)
async def perform_query(request: httpx.Request) -> dict[str, Any]:
    token = os.getenv("IMMOWELT_RESIDENTIAL_SEARCH_TOKEN")
    if not token:
        raise NoTokenFoundError()

    request.headers["Authorization"] = f"Bearer {token}"
    url = "https://api.immowelt.com/residentialsearch/v1/searches"

    async with httpx.AsyncClient(http2=True) as client:
        response = await client.send(request)
    return response.json()
