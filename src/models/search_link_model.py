from typing import TYPE_CHECKING
from enum import (
  Enum,
  IntEnum,
)
from sqlalchemy import (
  BigInteger,
  SmallInteger,
  Text,
  String,
  Boolean,
)
from sqlalchemy.orm import (
  mapped_column,
  relationship,
  Mapped,
)
from sqlalchemy.sql import expression
from .base_model import BaseModel
if TYPE_CHECKING:
  from .user_model import UserModel
  from .user_search_link_model import UserSearchLinkModel

# ! FIX: duplicate from src.api.search_links.search_links_types cause its cycle import
class SearchType(IntEnum):
  rent = 1
  purchase = 2

class SourceName(Enum):
  avito = "avito"
  yandex = "yandex"
  cian = "cian"

class SearchLinkModel(BaseModel):
  __tablename__ = "search_links"

  id: Mapped[int] = mapped_column(
    BigInteger,
    primary_key=True,
    autoincrement=True,
  )

  search_type: Mapped[int] = mapped_column(
    SmallInteger,
  )

  @property
  def search_type_enum(self) -> SearchType:
    for _, enum_value in SearchType.__members__.items():
      if enum_value.value == self.search_type:
        return enum_value

    raise ValueError()

  search_link: Mapped[str] = mapped_column(
    Text,
  )

  source_name: Mapped[str] = mapped_column(
    Text,
  )

  @property
  def source_name_enum(self) -> SourceName:
    return SourceName[self.source_name]

  is_active: Mapped[bool] = mapped_column(
    Boolean,
    server_default=expression.true(),
  )

  name: Mapped[str] = mapped_column(
    String(64),
  )

  # m2m
  users: Mapped[list["UserModel"]] = relationship(
    back_populates="search_links",
    secondary="users_search_links",
  )
  # o2m
  search_link_users_search_links_associations: Mapped[list["UserSearchLinkModel"]] = relationship(
    back_populates="search_link",
    viewonly=True,
  )
