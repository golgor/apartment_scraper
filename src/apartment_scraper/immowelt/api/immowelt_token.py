import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Any, Callable

import httpx
from dotenv import set_key
from pydantic import BaseModel
from result import Err, as_result


class ImmoweltTokenRequestResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    iss: str
    creation_offset_date_time: datetime
    iat: int
    tenant: str
    jti: str


@as_result(Exception)
def get_token() -> ImmoweltTokenRequestResponse:
    url = "https://api.immowelt.com/auth/oauth/token"
    header = {
        "content-type": "application/x-www-form-urlencoded",
        "accept": "application/json, text/plain, */*",
        "authorization": os.getenv("IMMOWELT_AUTH_REQUEST_BEARER_TOKEN", ""),
    }
    data = {"grant_type": "client_credentials"}

    with httpx.Client() as client:
        response = client.post(url=url, data=data, headers=header)
        response.raise_for_status()

    return ImmoweltTokenRequestResponse.model_validate(response.json())


def with_token(func: Callable[..., Any]):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = os.getenv("IMMOWELT_RESIDENTIAL_SEARCH_TOKEN")
        expiration_datetime = os.getenv(
            "IMMOWELT_RESIDENTIAL_SEARCH_TOKEN_EXPIRATION_DATETIME", 0
        )
        if not token or datetime.now() > datetime.fromtimestamp(
            int(expiration_datetime)
        ) + timedelta(hours=1):
            token_result = get_token()
            if isinstance(token_result, Err):
                raise token_result.err()

            token = token_result.unwrap()
            set_key(
                dotenv_path=".env",
                key_to_set="IMMOWELT_RESIDENTIAL_SEARCH_TOKEN",
                value_to_set=token.access_token,
            )
            set_key(
                dotenv_path=".env",
                key_to_set="IMMOWELT_RESIDENTIAL_SEARCH_TOKEN_EXPIRATION_DATETIME",
                value_to_set=str(int(token.creation_offset_date_time.timestamp())),
            )

        return func(*args, **kwargs)

    return wrapper


@with_token
def test():
    bearer_token = os.getenv("IMMOWELT_RESIDENTIAL_SEARCH_TOKEN")
    print(bearer_token)


if __name__ == "__main__":
    test()
