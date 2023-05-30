import csv
import pathlib
from typing import Any, NamedTuple, Optional

from sqlalchemy import (
    Column,
    DateTime,
    column,
    create_engine,
    func,
    select,
    table,
    update,
)
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class TransactionResult(NamedTuple):
    data: Any
    element_count: int
    total_count: int


class Base(DeclarativeBase):
    pass


class Apartment(Base):
    __tablename__ = "apartments"
    id: Mapped[int] = mapped_column(primary_key=True)
    apartment_id: Mapped[int]
    status: Mapped[bool]
    product_id: Mapped[str]
    property_type: Mapped[str]
    area: Mapped[int]
    url: Mapped[str]
    rooms: Mapped[float]
    floor: Mapped[int]
    address: Mapped[str]
    post_code: Mapped[str]
    location: Mapped[str]
    coordinates: Mapped[Optional[str]]
    price: Mapped[Optional[int]]
    price_per_area: Mapped[Optional[float]]
    free_area_type = Column(JSON, nullable=True)
    free_area = Column(JSON, nullable=True)
    image_urls = Column(JSON, nullable=True)
    advertiser: Mapped[str]
    prio: Mapped[Optional[int]]
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class Model:
    def __init__(self, path: pathlib.Path) -> None:
        self.engine = create_engine(
            f"sqlite:///{str(path)}",
            echo=False,
            connect_args={"check_same_thread": False},
        )
        if not path.exists():
            print("Creating database!")
            Base.metadata.create_all(self.engine)

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
