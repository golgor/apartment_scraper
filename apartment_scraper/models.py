import pathlib
from typing import List, Optional

from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
)

from apartment_scraper import pkg_path


class Base(DeclarativeBase):
    pass


class Apartments(Base):
    __tablename__ = "apartments"
    id: Mapped[int] = mapped_column(primary_key=True)
    apartment_id: Mapped[int]
    area: Mapped[int]
    price: Mapped[int]
    rooms: Mapped[float]
    floor: Mapped[int]
    post_code: Mapped[str]
    price_per_area: Mapped[float]


class Model:
    def __init__(self, path: pathlib.Path):
        self.engine = create_engine(f"sqlite:///{str(path)}", echo=True)
        if not path.exists():
            print("Creating database!")
            Base.metadata.create_all(self.engine)
        print("Database found!")

    def add_apartment(self):
        with Session(self.engine) as session:
            spongebob = Apartments(
                apartment_id=1,
                area=1,
                price=1,
                rooms=1.5,
                floor=1,
                post_code="15124",
                price_per_area=15.4,
            )

            session.add(spongebob)
            session.commit()


if __name__ == "__main__":
    model = Model(path=pkg_path.joinpath("test.db"))
    model.add_apartment()
