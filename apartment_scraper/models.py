import pathlib
from datetime import datetime
from typing import TYPE_CHECKING, Any, NamedTuple, Optional
from zoneinfo import ZoneInfo

from sqlmodel import Field, Session, SQLModel, create_engine

from apartment_scraper import pkg_path


if TYPE_CHECKING:
    from sqlalchemy.future.engine import Engine


class TransactionResult(NamedTuple):
    data: Any
    element_count: int
    total_count: int


class Apartment(SQLModel, table=True):
    __tablename__ = "apartments"
    id: Optional[int] = Field(default=None, primary_key=True)
    apartment_id: int
    status: bool
    product_id: str
    property_type: str
    area: int
    url: str
    rooms: float
    floor: int
    address: str
    post_code: str
    location: str
    coordinates: str | None
    price: float | None
    price_per_area: float | None
    free_area_type: Optional[str]
    free_area: Optional[str]
    image_urls: Optional[str]
    advertiser: str
    prio: Optional[int]
    updated: Optional[datetime] = Field(
        default=datetime.now(tz=ZoneInfo("UTC"))
    )


class Model:
    def __init__(self, path: pathlib.Path) -> None:
        self.engine = create_engine(f"sqlite:///{str(path)}", echo=False)
        if not path.exists():
            print("Creating database!")
            SQLModel.metadata.create_all(self.engine)

    def get_engine(self) -> "Engine":
        return self.engine

    def add_apartment(self, apartment: Apartment) -> None:
        with Session(self.engine) as session:
            session.add(apartment)
            session.commit()

    def add_apartments(self, apartments: list[Apartment]) -> None:
        with Session(self.engine) as session:
            session.add_all(apartments)
            session.commit()

    def get_map_data(self) -> list[Apartment]:
        stmt = select(Apartment).filter(
            Apartment.post_code >= 1000,
            Apartment.post_code < 2000,
            Apartment.rooms >= 3,
            Apartment.price <= 400_000,
            Apartment.price > 0,
            Apartment.product_id != "project",
        )
        with Session(self.engine) as session:
            return list(session.scalars(stmt))

    def get_paged_apartments(self, page: int, pagesize: int) -> TransactionResult:
        stmt = select(Apartment).where(Apartment.id > page * pagesize).limit(pagesize)

        my_table = table("apartments", column("id"))
        count = select(func.count()).select_from(my_table)
        with Session(self.engine) as session:
            total_count = session.execute(count).scalar()
            results = list(session.scalars(stmt))
        return TransactionResult(results, len(results), total_count or 0)

    def get_apartment_by_id(self, apartment_id: int) -> Apartment | None:
        stmt = select(Apartment).where(Apartment.apartment_id == apartment_id)

        with Session(self.engine) as session:
            apartment: Apartment | None = session.scalars(stmt).first()
        return apartment

    def get_count(self) -> int:
        with Session(self.engine) as session:
            return session.query(Apartment).count()

    def update_apartment_prio(self, apartment_id: int, prio: int) -> Apartment | None:
        stmt = (
            update(Apartment)
            .where(Apartment.apartment_id == apartment_id)
            .values(prio=prio)
            .returning(Apartment)
        )

        with Session(self.engine) as session:
            result = session.execute(stmt).scalar_one_or_none()
            if result:
                session.expunge(result)
            session.commit()
        return result


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
        post_code="test",
        location="test",
        coordinates="test",
        price=1,
        price_per_area=1,
        free_area_type="test",
        free_area="test",
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
        post_code="test",
        location="test",
        coordinates="test",
        price=1,
        price_per_area=1,
        free_area_type="test",
        free_area="test",
        image_urls="test",
        advertiser="test",
        prio=1,
    )
    model = Model(path=pkg_path.joinpath("test.db"))
    model.add_apartments([apartment, apartment2])
