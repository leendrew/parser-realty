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
  from . import ParsingResultModel

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

  metro_station_id: Mapped[int] = mapped_column(
    SmallInteger,
    ForeignKey(
      "metro_stations.id",
      ondelete="CASCADE",
    ),
  )

  # o2o
  parsing_result: Mapped["ParsingResultModel"] = relationship(
    back_populates="city_metro_station",
  )
