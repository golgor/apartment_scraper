import os
from collections.abc import Callable
from datetime import datetime, timedelta
from functools import wraps
from typing import Any
from zoneinfo import ZoneInfo

import httpx
from dotenv import set_key
from pydantic import BaseModel
from result import Err, as_result


class ImmoweltTokenRequestResponse(BaseModel):
    """A BaseModel for the response from the Immowelt Auth API."""

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
    """Get a token for the immowelt api.

    The Immowelt API for searching for apartments requires an access token. This token is obtained by sending a POST
    request to another endpoint. The acquired token is valid for 1 hour.

    Returns:
        ImmoweltTokenRequestResponse: A parsed response from the Immowelt Auth API.
    """
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
    """Decorator for making sure that the token is valid before calling a function.

    If the token does not exist, or is expired, the decorator will call the get_token function to get a new token.
    The new token will be set in a .env-file and update the variables in the environment.

    Args:
        func (Callable[..., Any]): A callable function

    Raises:
        token_result.err: If the token could not be retrieved

    Returns:
        The result of the decorated function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        token = os.getenv("IMMOWELT_RESIDENTIAL_SEARCH_TOKEN")
        expiration_datetime = os.getenv("IMMOWELT_RESIDENTIAL_SEARCH_TOKEN_EXPIRATION_DATETIME", "0")

        # If token does not exist, or is expired. A token is valid for 1 hour.
        if not token or datetime.now(tz=ZoneInfo("UTC")) > datetime.fromtimestamp(
            int(expiration_datetime), tz=ZoneInfo("UTC")
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
