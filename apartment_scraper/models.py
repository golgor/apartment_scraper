import csv
import pathlib
from typing import Any, Generator, NamedTuple, Optional

from sqlalchemy import (
    Column,
    DateTime,
    column,
    create_engine,
    func,
    select,
    table,
)
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)


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
    product_id: Mapped[int]
    area: Mapped[int]
    url: Mapped[str]
    rooms: Mapped[float]
    floor: Mapped[int]
    address: Mapped[str]
    post_code: Mapped[str]
    coordinates: Mapped[Optional[str]]
    free_area_type = Column(JSON, nullable=True)
    free_area = Column(JSON, nullable=True)
    image_urls = Column(JSON, nullable=True)
    apartment_type: Mapped[str]
    advertiser: Mapped[str]
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
    __mapper_args__ = {"polymorphic_on": "apartment_type"}


class ApartmentBuy(Apartment):
    __mapper_args__ = {"polymorphic_identity": "purchase"}
    price: Mapped[Optional[int]]
    price_per_area: Mapped[Optional[float]]


class ApartmentRent(Apartment):
    __mapper_args__ = {"polymorphic_identity": "rental"}
    rent: Mapped[Optional[int]]
    rent_per_area: Mapped[Optional[float]]

    def __repr__(self) -> str:
        return f"ApartmentsRent(id={self.id}, apartment_id={self.apartment_id}, area={self.area}, rent={self.rent}, url={self.url}, rooms={self.rooms}, floor={self.floor}, post_code={self.post_code}, rent_per_area={self.rent_per_area}, image_urls={self.image_urls}, created={self.created}, updated={self.updated})"


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

    def get_db_session(self) -> Generator[Session, None, None]:
        db = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )()
        try:
            yield db
        finally:
            db.close()
        return

    def add_apartment(self, apartment: ApartmentBuy) -> None:
        with Session(self.engine) as session:
            session.add(apartment)
            session.commit()

    def add_apartments(
        self, apartments: list[ApartmentBuy] | list[ApartmentRent]
    ) -> None:
        with Session(self.engine) as session:
            session.add_all(apartments)
            session.commit()

    def get_rentals(self, page: int, pagesize: int) -> TransactionResult:
        stmt = (
            select(ApartmentRent)
            .where(ApartmentRent.id > page * pagesize)
            .limit(pagesize)
        )

        my_table = table("apartments", column("id"))
        count = select(func.count()).select_from(my_table)
        with Session(self.engine) as session:
            total_count = session.execute(count).scalar()
            results = list(session.scalars(stmt))
        return TransactionResult(results, len(results), total_count or 0)

    def get_freiwohnungen(self) -> list[ApartmentBuy]:
        stmt = select(ApartmentBuy)

        with Session(self.engine) as session:
            return list(session.scalars(stmt).all())

    def get_count(self) -> int:
        with Session(self.engine) as session:
            return session.query(ApartmentBuy).count()

    def dump_to_csv(self, filename: str) -> None:
        with Session(self.engine) as session:
            with open("dump.csv", "w") as f:
                out = csv.writer(f)
                out.writerow(
                    [
                        "apartment_id",
                        "area",
                        "rent",
                        "url",
                        "rooms",
                        "floor",
                        "address",
                        "post_code",
                        "rent_per_area",
                        "coordinates",
                        "free_area_type",
                        "free_area",
                    ]
                )

                for item in session.query(ApartmentRent).all():
                    out.writerow(
                        [
                            item.apartment_id,
                            item.area,
                            item.rent,
                            item.url,
                            item.rooms,
                            item.floor,
                            item.address,
                            item.post_code,
                            item.rent_per_area,
                            item.coordinates,
                            item.free_area_type,
                            item.free_area,
                        ]
                    )
