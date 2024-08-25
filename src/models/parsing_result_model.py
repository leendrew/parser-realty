from typing import (
  Optional,
  TYPE_CHECKING,
)
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
  func,
)
from src.api.parsing_results.parsing_result_types import HousingType
from .base_model import BaseModel
if TYPE_CHECKING:
  from .user_search_link_model import UserSearchLinkModel
  from .city_metro_station_model import CityMetroStationModel

class ParsingResultModel(BaseModel):
  __tablename__ = "parsing_results"

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
    ForeignKey(
      "users_search_links.id",
      ondelete="CASCADE",
    ),
  )
  # m2o
  user_search_link: Mapped["UserSearchLinkModel"] = relationship(
    back_populates="parsing_results",
  )

  city_metro_station_id: Mapped[int | None] = mapped_column(
    SmallInteger,
    ForeignKey("cities_metro_stations.id"),
    nullable=True,
  )
  # o2o
  city_metro_station: Mapped[Optional["CityMetroStationModel"]] = relationship(
    back_populates="parsing_result",
  )

  direct_link: Mapped[str] = mapped_column(
    Text,
    index=True,
  )

  housing_type: Mapped[HousingType] = mapped_column(
    Text,
  )

  flat_room_type: Mapped[int] = mapped_column(
    SmallInteger,
    comment="0 - студия",
  )

  floor: Mapped[str] = mapped_column(
    String(5),
  )

  flat_area: Mapped[str] = mapped_column(
    String(7),
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
