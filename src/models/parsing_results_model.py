from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy.orm import (
  mapped_column,
  relationship,
  Mapped,
)
from sqlalchemy import (
  ForeignKey,
  BigInteger,
  SmallInteger,
  Text,
  String,
  DateTime,
  Float,
  func,
)
from src.api.parsing_results.parsing_results_types import HousingType
from .base_model import BaseModel
if TYPE_CHECKING:
  from . import UsersSearchLinksModel
  from . import CitiesMetroStationsModel

class ParsingResults(BaseModel):
  id: Mapped[int] = mapped_column(
    BigInteger,
    primary_key=True,
    autoincrement=True,
  )

  created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    server_default=func.now(),
  )

  user_search_link_id: Mapped[int] = mapped_column(
    BigInteger,
    ForeignKey("users_search_links.id"),
  )
  # o2o
  user_search_link: Mapped["UsersSearchLinksModel"] = relationship(
    back_populates="parsing_result",
  )

  city_metro_station_id: Mapped[int | None] = mapped_column(
    SmallInteger,
    ForeignKey("cities_metro_stations.id"),
    nullable=True,
  )
  # o2o
  city_metro_station: Mapped["CitiesMetroStationsModel"] = relationship(back_populates="")

  direct_link: Mapped[str] = mapped_column(
    Text,
  )

  listed_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
  )

  housing_type: Mapped[HousingType] = mapped_column(
    Text,
  )

  flat_room_type: Mapped[int] = mapped_column(
    SmallInteger,
    comment="0 - studio",
  )

  floor: Mapped[str] = mapped_column(
    String(5),
  )

  flat_area: Mapped[float] = mapped_column(
    Float,
  )

  price: Mapped[int] = mapped_column(
    BigInteger,
  )

  commission_percent: Mapped[int] = mapped_column(
    SmallInteger,
  )

  deposit_percent: Mapped[int] = mapped_column(
    SmallInteger,
  )
