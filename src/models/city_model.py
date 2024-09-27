from typing import TYPE_CHECKING
from sqlalchemy import (
  SmallInteger,
  Text,
)
from sqlalchemy.orm import (
  mapped_column,
  relationship,
  Mapped,
)
from .base_model import BaseModel
if TYPE_CHECKING:
  from .metro_station_model import MetroStationModel
  from .city_metro_station_model import CityMetroStationModel

class CityModel(BaseModel):
  __tablename__ = "cities"

  id: Mapped[int] = mapped_column(
    SmallInteger,
    primary_key=True,
    autoincrement=True,
  )

  name: Mapped[str] = mapped_column(
    Text,
  )

  # m2m
  metro_stations: Mapped[list["MetroStationModel"]] = relationship(
    back_populates="cities",
    secondary="cities_metro_stations",
  )
  # o2m
  city_cities_metro_stations_associations: Mapped[list["CityMetroStationModel"]] = relationship(
    back_populates="city",
    viewonly=True,
  )
