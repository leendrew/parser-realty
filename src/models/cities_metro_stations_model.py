from typing import TYPE_CHECKING
from sqlalchemy.orm import (
  mapped_column,
  relationship,
  Mapped,
)
from sqlalchemy import (
  ForeignKey,
  SmallInteger,
)
from .base_model import BaseModel
if TYPE_CHECKING:
  from . import CitiesModel
  from . import MetroStationsModel

class CitiesMetroStations(BaseModel):
  id: Mapped[int] = mapped_column(
    SmallInteger,
    primary_key=True,
    autoincrement=True,
  )

  city_id: Mapped[int] = mapped_column(
    SmallInteger,
    ForeignKey("cities.id"),
  )
  # m2m
  cities: Mapped[list["CitiesModel"]] = relationship(
    back_populates="metro_stations",
  )

  metro_station_id: Mapped[int] = mapped_column(
    SmallInteger,
    ForeignKey("metro_stations.id"),
  )
  # m2m
  metro_stations: Mapped[list["MetroStationsModel"]] = relationship(
    back_populates="cities",
  )
