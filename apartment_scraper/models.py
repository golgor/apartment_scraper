import os
from datetime import datetime
from typing import TYPE_CHECKING, NamedTuple, Self
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from loguru import logger
from sqlalchemy.engine import URL
from sqlmodel import Field, Session, SQLModel, create_engine, select, update


load_dotenv()

if TYPE_CHECKING:
    from sqlalchemy.engine.cursor import CursorResult
    from sqlalchemy.future.engine import Engine


class Apartment(SQLModel, table=True):
    """The main model to store apartments in the database."""

    __tablename__ = "apartments"
    id: int | None = Field(default=None, primary_key=True)  # noqa: A003
    apartment_id: int
    status: bool
    product_id: str
    property_type: str
    area: int
    url: str
    rooms: float
    floor: float
    address: str
    post_code: int
    location: str
    coordinates: str | None
    price: float
    price_per_area: float | None
    free_area_type: str | None
    free_area: int | None
    image_urls: str | None
    advertiser: str
    prio: int = 0
    updated: datetime | None = Field(default=datetime.now(tz=ZoneInfo("UTC")))


class TransactionResult(NamedTuple):
    """Named tuple to group the results of a transaction."""

    data: list[Apartment]
    element_count: int
    total_count: int


class Model:
    """A class to manage the database."""

    def __init__(self: Self) -> None:
        """Initialize the database.

        Creates an engine and the database if it does not exist.
        """
        url_object = URL.create(
            "postgresql",
            username=from_env("USERNAME"),
            password=from_env("PASSWORD"),
            host=from_env("HOST"),
            database=from_env("DATABASE"),
        )
        self.engine = create_engine(url_object)
        SQLModel.metadata.create_all(self.engine)

    def get_engine(self: Self) -> "Engine":
        """Get the engine.

        If the engine is needed somewhere else in another context.

        Returns:
            Engine: The engine of the initialized database.
        """
        return self.engine

    def add_apartment(self: Self, apartment: Apartment) -> None:
        """Add a single Apartment to the database.

        Args:
            apartment (Apartment): An apartment object.
        """
        with Session(self.engine) as session:
            session.add(apartment)
            session.commit()

    def add_apartments(self: Self, apartments: list[Apartment]) -> None:
        """Add several apartments to the database.

        Args:
            apartments (list[Apartment]): A list of Apartment objects
        """
        with Session(self.engine) as session:
            session.add_all(apartments)
            session.commit()

    def get_map_data(self: Self) -> list[Apartment]:
        """Export all apartments to a mapping function.

        Several filters are applied to the data to make it more useful.

        Returns:
            list[Apartment]: A list of Apartment objects.
        """
        stmt = select(Apartment).filter(
            Apartment.post_code >= 1000,  # noqa: PLR2004
            Apartment.post_code < 2000,  # noqa: PLR2004
            Apartment.rooms >= 3,  # noqa: PLR2004
            Apartment.price <= 400_000,  # noqa: PLR2004
            Apartment.price > 0,
            Apartment.product_id != "project",
        )
        with Session(self.engine) as session:
            return list(session.scalars(stmt))

    def get_paged_apartments(self: Self, page: int, pagesize: int) -> TransactionResult:
        """Get a page of apartments.

        This is used to get a "page" of apartments from the database. This is used to paginate the database and to avoid
        dumping the whole database in one query.

        Args:
            self (Self): _description_
            page (int): _description_
            pagesize (int): _description_

        Returns:
            TransactionResult: _description_
        """
        stmt = select(Apartment).where(Apartment.id > page * pagesize).limit(pagesize)

        with Session(self.engine) as session:
            total_count = session.query(Apartment).count()
            results: list[Apartment] = list(session.scalars(stmt))
        return TransactionResult(results, len(results), total_count or 0)

    def get_apartment_by_id(self: Self, apartment_id: int) -> Apartment | None:
        """Get details about a single apartment.

        Args:
            apartment_id (int): The id of an apartment.

        Returns:
            Apartment | None: An Apartment object or None if the apartment does not exist.
        """
        stmt = select(Apartment).where(Apartment.apartment_id == apartment_id)

        with Session(self.engine) as session:
            apartment: Apartment | None = session.scalars(stmt).first()
        return apartment

    def get_count(self: Self) -> int:
        """Get the number of apartments in the database."""
        with Session(self.engine) as session:
            return session.query(Apartment).count()

    def update_apartment_prio(self: Self, apartment_id: int, prio: int) -> bool:
        """Update the priority of an apartment.

        Args:
            apartment_id (int): The id of an apartment.
            prio (int): The new priority of the apartment.

        Returns:
            Apartment | None: Returns the updated apartment or None if the apartment does not exist.
        """
        stmt = (
            update(Apartment)
            .where(Apartment.apartment_id == apartment_id)
            .values(prio=prio)
        )

        with Session(self.engine) as session:
            result: "CursorResult" = session.execute(stmt)
            row_count: int = result.rowcount
            session.commit()

        return bool(row_count)


def from_env(name: str) -> str:
    """Get an environment variable.

    Args:
        name (str): The name of the environment variable.

    Raises:
        KeyError: If the environment variable does not exist.

    Returns:
        str: The value of the environment variable.
    """
    try:
        return os.environ[name]
    except KeyError as e:
        logger.error(f"Environment variable {name} does not exist.")
        raise KeyError() from e


if __name__ == "__main__":
    apartment = Apartment(
        apartment_id=1,
        status=False,
        product_id="1",
        property_type="test",
        area=1,
        url="test",
        rooms=1,
        floor=1,
        address="test",
        post_code=123,
        location="test",
        coordinates="test",
        price=1,
        price_per_area=1,
        free_area_type="test",
        free_area=0,
        image_urls="test",
        advertiser="test",
        prio=1,
    )
    apartment2 = Apartment(
        apartment_id=13563,
        status=False,
        product_id="1",
        property_type="test",
        area=1,
        url="test",
        rooms=1,
        floor=1,
        address="test",
        post_code=12345,
        location="test",
        coordinates="test",
        price=1,
        price_per_area=1,
        free_area_type="test",
        free_area=0,
        image_urls="test",
        advertiser="test",
        prio=1,
    )
    model = Model()
    model.add_apartments([apartment, apartment2])
