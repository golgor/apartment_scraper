import csv
import pathlib
from typing import Any, NamedTuple, Optional
from sqlmodel import Field, SQLModel, create_engine
from datetime import datetime
from zoneinfo import ZoneInfo
from apartment_scraper import pkg_path


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
    prio: int | None
    updated: Optional[datetime] = Field(
        default=datetime.now(tz=ZoneInfo("UTC"))
    )


class Model:
    def __init__(self, path: pathlib.Path) -> None:
        self.engine = create_engine(f"sqlite:///{str(path)}", echo=False)
        if not path.exists():
            print("Creating database!")
            SQLModel.metadata.create_all(self.engine)

    def get_engine(self):
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
            results = list(session.scalars(stmt))
        return results

    def get_paged_apartments(
        self, page: int, pagesize: int
    ) -> TransactionResult:
        stmt = (
            select(Apartment)
            .where(Apartment.id > page * pagesize)
            .limit(pagesize)
        )

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

    def update_apartment_prio(
        self, apartment_id: int, prio: int
    ) -> Apartment | None:
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

    def dump_to_csv(self, filename: str) -> None:
        with Session(self.engine) as session:
            with open("dump.csv", "w") as f:
                out = csv.writer(f)
                out.writerow(
                    [
                        "apartment_id",
                        "area",
                        "price",
                        "url",
                        "rooms",
                        "floor",
                        "address",
                        "post_code",
                        "price_per_area",
                        "coordinates",
                        "free_area_type",
                        "free_area",
                    ]
                )

                for item in session.query(Apartment).all():
                    out.writerow(
                        [
                            item.apartment_id,
                            item.area,
                            item.price,
                            item.url,
                            item.rooms,
                            item.floor,
                            item.address,
                            item.post_code,
                            item.price_per_area,
                            item.coordinates,
                            item.free_area_type,
                            item.free_area,
                        ]
                    )


if __name__ == "__main__":
    model = Model(path=pkg_path.joinpath("test.db"))
