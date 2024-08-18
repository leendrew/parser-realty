from typing import TYPE_CHECKING
from sqlalchemy.orm import (
  mapped_column,
  relationship,
  Mapped,
)
from sqlalchemy import (
  SmallInteger,
  Text,
)
from .base_model import BaseModel
if TYPE_CHECKING:
  from . import CitiesModel
  from . import CitiesMetroStationsModel

class MetroStations(BaseModel):
  id: Mapped[int] = mapped_column(
    SmallInteger,
    primary_key=True,
    autoincrement=True,
  )

  name: Mapped[str] = mapped_column(
    Text,
  )

  color: Mapped[str] = mapped_column(
    Text,
  )

  # m2m
  cities: Mapped[list["CitiesModel"]] = relationship(
    back_populates="metro_stations",
    secondary="cities_metro_stations",
  )

  # o2m
  city_metro_stations: Mapped[list["CitiesMetroStationsModel"]] = relationship(
    back_populates="metro_station",
  )