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
  from .parsing_result_model import ParsingResultModel
  from .city_model import CityModel
  from .metro_station_model import MetroStationModel

class CityMetroStationModel(BaseModel):
  __tablename__ = "cities_metro_stations"

  id: Mapped[int] = mapped_column(
    SmallInteger,
    primary_key=True,
    autoincrement=True,
  )

  city_id: Mapped[int] = mapped_column(
    SmallInteger,
    ForeignKey(
      "cities.id",
      ondelete="CASCADE",
    ),
  )
  # m2o
  city: Mapped["CityModel"] = relationship(
    back_populates="city_cities_metro_stations_associations",
    viewonly=True,
  )

  metro_station_id: Mapped[int] = mapped_column(
    SmallInteger,
    ForeignKey(
      "metro_stations.id",
      ondelete="CASCADE",
    ),
  )
  # m2o
  metro_station: Mapped["MetroStationModel"] = relationship(
    back_populates="metro_station_cities_metro_stations_associations",
    viewonly=True,
  )

  # o2o
  parsing_result: Mapped["ParsingResultModel"] = relationship(
    back_populates="city_metro_station",
  )
