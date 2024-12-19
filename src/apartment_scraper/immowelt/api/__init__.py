from typing import Any

import httpx
from dotenv import load_dotenv
from result import as_async_result

from apartment_scraper.immowelt.api.immowelt_token import get_token

load_dotenv()


@as_async_result(Exception)
async def perform_query(
    request: httpx.Request, bearer_token: str = ""
) -> dict[str, Any]:
    request.headers["Authorization"] = f"Bearer {bearer_token}"
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.send(request)
    return response.json()
