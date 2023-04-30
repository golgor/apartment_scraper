import csv
import datetime
import pathlib
from typing import Optional

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    create_engine,
    func,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from apartment_scraper import pkg_path


class Base(DeclarativeBase):
    pass


class ApartmentBuy(Base):
    __tablename__ = "apartments_buy"
    id: Mapped[int] = mapped_column(primary_key=True)
    apartment_id: Mapped[int]
    area: Mapped[int]
    price: Mapped[int]
    url: Mapped[str]
    rooms: Mapped[float]
    floor: Mapped[int]
    address: Mapped[str]
    post_code: Mapped[str]
    price_per_area: Mapped[float]
    image_urls: Mapped[Optional[str]]
    site: Mapped[str] = mapped_column(ForeignKey("site_info.site"))
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class ApartmentRent(Base):
    __tablename__ = "apartments_rent"
    id: Mapped[int] = mapped_column(primary_key=True)
    apartment_id: Mapped[int]
    area: Mapped[int]
    rent: Mapped[int]
    url: Mapped[str]
    rooms: Mapped[float]
    floor: Mapped[int]
    address: Mapped[str]
    post_code: Mapped[str]
    rent_per_area: Mapped[float]
    image_urls: Mapped[Optional[str]]
    site: Mapped[str] = mapped_column(ForeignKey("site_info.site"))
    coordinates: Mapped[Optional[str]]
    free_area_type: Mapped[Optional[str]]
    free_area: Mapped[Optional[int]]
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self) -> str:
        return f"ApartmentsRent(id={self.id}, apartment_id={self.apartment_id}, area={self.area}, rent={self.rent}, url={self.url}, rooms={self.rooms}, floor={self.floor}, post_code={self.post_code}, rent_per_area={self.rent_per_area}, image_urls={self.image_urls}, site={self.site}, created={self.created}, updated={self.updated})"


class SiteInfo(Base):
    __tablename__ = "site_info"
    site: Mapped[str] = mapped_column(primary_key=True)
    url_base: Mapped[str]
    image_base: Mapped[str]


class Model:
    def __init__(self, path: pathlib.Path) -> None:
        self.engine = create_engine(f"sqlite:///{str(path)}", echo=False)
        if not path.exists():
            print("Creating database!")
            Base.metadata.create_all(self.engine)

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

    def add_site(self, site: SiteInfo) -> None:
        with Session(self.engine) as session:
            session.add(site)
            session.commit()

    def get_apartments(self, date: Optional[datetime.date] = None) -> None:
        if date:
            stmt = select(ApartmentBuy).where(
                func.DATE(ApartmentBuy.created) == str(date)
            )
        else:
            stmt = select(ApartmentBuy)

        with Session(self.engine) as session:
            for apartment in session.scalars(stmt):
                print(apartment.apartment_id)

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
                        "site",
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
                            item.site,
                            item.coordinates,
                            item.free_area_type,
                            item.free_area,
                        ]
                    )


def add_willhaben_siteinfo(model: Model) -> None:
    willhaben = SiteInfo(
        site="willhaben",
        url_base="https://www.willhaben.at/iad/",
        image_base="https://cache.willhaben.at/mmo/",
    )
    model.add_site(willhaben)


if __name__ == "__main__":
    model = Model(path=pkg_path.joinpath("test.db"))
    date = datetime.date(2023, 2, 17)
    # add_willhaben_siteinfo(model)
    add_willhaben_siteinfo(model)
