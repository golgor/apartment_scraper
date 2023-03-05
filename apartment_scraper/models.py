import datetime
import json
import pathlib
from typing import Any, Optional

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    String,
    create_engine,
    func,
    select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from apartment_scraper import pkg_path


class Base(DeclarativeBase):
    pass


class Apartment(Base):
    __tablename__ = "apartments"
    id: Mapped[int] = mapped_column(primary_key=True)
    apartment_id: Mapped[int]
    area: Mapped[int]
    price: Mapped[int]
    url: Mapped[str]
    rooms: Mapped[float]
    floor: Mapped[int]
    post_code: Mapped[str]
    price_per_area: Mapped[float]
    image_urls: Mapped[Optional[str]]
    site: Mapped[str] = mapped_column(ForeignKey("site_info.site"))
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


class SiteInfo(Base):
    __tablename__ = "site_info"
    site: Mapped[str] = mapped_column(primary_key=True)
    url_base: Mapped[str]
    image_base: Mapped[str]


class Model:
    def __init__(self, path: pathlib.Path):
        self.engine = create_engine(f"sqlite:///{str(path)}", echo=False)
        if not path.exists():
            print("Creating database!")
            Base.metadata.create_all(self.engine)

    def add_apartment(self, apartment: Apartment):
        with Session(self.engine) as session:
            session.add(apartment)
            session.commit()

    def add_apartments(self, apartments: list[Apartment]):
        with Session(self.engine) as session:
            session.add_all(apartments)
            session.commit()

    def add_site(self, site: SiteInfo):
        with Session(self.engine) as session:
            session.add(site)
            session.commit()

    def get_apartments(self, date: Optional[datetime.date] = None):
        if date:
            stmt = select(Apartment).where(
                func.DATE(Apartment.created) == str(date)
            )
        else:
            stmt = select(Apartment)

        with Session(self.engine) as session:
            for apartment in session.scalars(stmt):
                print(apartment.apartment_id)

    def get_count(self) -> int:
        with Session(self.engine) as session:
            return session.query(Apartment).count()


def add_willhaben_siteinfo(model: Model):
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
