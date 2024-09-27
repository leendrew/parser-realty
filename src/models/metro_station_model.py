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
  from .city_model import CityModel
  from .city_metro_station_model import CityMetroStationModel

class MetroStationModel(BaseModel):
  __tablename__ = "metro_stations"

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
  cities: Mapped[list["CityModel"]] = relationship(
    back_populates="metro_stations",
    secondary="cities_metro_stations",
  )
  # o2m
  metro_station_cities_metro_stations_associations: Mapped[list["CityMetroStationModel"]] = relationship(
    back_populates="metro_station",
    viewonly=True,
  )
