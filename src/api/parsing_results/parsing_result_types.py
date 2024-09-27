from typing import (
  Optional,
  TYPE_CHECKING,
)
from pydantic import BaseModel
if TYPE_CHECKING:
  from src.models.user_search_link_model import UserSearchLinkModel
  from src.models.city_metro_station_model import CityMetroStationModel

class ParsingResultBase(BaseModel):
  direct_link: str
  floor: str
  flat_area: str
  price: int
  commission_percent: int | None
  deposit_percent: int | None

class ParsingResult(ParsingResultBase):
  metro_station_name: str | None

class CreateOnePayload(ParsingResultBase):
  user_search_link: "UserSearchLinkModel"
  city_metro_station: Optional["CityMetroStationModel"]
