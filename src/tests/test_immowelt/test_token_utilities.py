from datetime import datetime, timedelta

import pytest
from result import Err, Ok

from apartment_scraper.immowelt.api.immowelt_token import with_token


class MockToken:
    def __init__(self, access_token, creation_offset_date_time):
        self.access_token = access_token
        self.creation_offset_date_time = creation_offset_date_time


@pytest.mark.parametrize(
    "existing_token,existing_expiration,expected_token",
    [
        pytest.param(
            "existing_valid_token",
            datetime.now().timestamp(),
            "existing_valid_token",
            id="valid_existing_token",
        ),
        pytest.param(
            "expired_token",
            (datetime.now() - timedelta(hours=2)).timestamp(),
            "new_token",
            id="expired_token",
        ),
    ],
)
def test_with_token_decorator(
    monkeypatch, existing_token, existing_expiration, expected_token
):
    # Arrange
    def mock_get_token():
        return Ok(
            MockToken(
                access_token="new_token", creation_offset_date_time=datetime.now()
            )
        )

    mock_set_key_calls = []

    def mock_set_key(dotenv_path, key_to_set, value_to_set):
        mock_set_key_calls.append((key_to_set, value_to_set))

    @with_token
    def dummy_function():
        return "function_called"

    monkeypatch.setenv("IMMOWELT_RESIDENTIAL_SEARCH_TOKEN", existing_token)
    monkeypatch.setenv(
        "IMMOWELT_RESIDENTIAL_SEARCH_TOKEN_EXPIRATION_DATETIME",
        str(int(existing_expiration)),
    )
    monkeypatch.setattr(
        "apartment_scraper.immowelt.api.immowelt_token.get_token", mock_get_token
    )
    monkeypatch.setattr(
        "apartment_scraper.immowelt.api.immowelt_token.set_key", mock_set_key
    )

    # Act
    result = dummy_function()

    # Assert
    assert result == "function_called"
    if existing_token != expected_token:
        assert len(mock_set_key_calls) == 2
        assert mock_set_key_calls[0][0] == "IMMOWELT_RESIDENTIAL_SEARCH_TOKEN"
        assert (
            mock_set_key_calls[1][0]
            == "IMMOWELT_RESIDENTIAL_SEARCH_TOKEN_EXPIRATION_DATETIME"
        )


def test_with_token_get_token_error(monkeypatch):
    # Arrange
    def mock_get_token():
        return Err(ValueError("Token error"))

    @with_token
    def dummy_function():
        return "function_called"

    monkeypatch.setenv("IMMOWELT_RESIDENTIAL_SEARCH_TOKEN", "")
    monkeypatch.setenv("IMMOWELT_RESIDENTIAL_SEARCH_TOKEN_EXPIRATION_DATETIME", "0")
    monkeypatch.setattr(
        "apartment_scraper.immowelt.api.immowelt_token.get_token", mock_get_token
    )

    # Act & Assert
    with pytest.raises(ValueError, match="Token error"):
        dummy_function()
