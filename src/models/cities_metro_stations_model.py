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
  from . import ParsingResultsModel

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
  # m2o
  city: Mapped["CitiesModel"] = relationship(
    back_populates="city_metro_stations",
  )

  metro_station_id: Mapped[int] = mapped_column(
    SmallInteger,
    ForeignKey("metro_stations.id"),
  )
  # m2o
  metro_station: Mapped["MetroStationsModel"] = relationship(
    back_populates="city_metro_stations",
  )

  # o2o
  parsing_result: Mapped["ParsingResultsModel"] = relationship(
    back_populates="city_metro_station",
  )
