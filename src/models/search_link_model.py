from typing import TYPE_CHECKING
from sqlalchemy.orm import (
  mapped_column,
  relationship,
  Mapped,
)
from sqlalchemy import (
  BigInteger,
  Text,
  String,
  Boolean,
)
from sqlalchemy.sql import expression
from src.api.search_links.search_link_types import SourceName
from .base_model import BaseModel
if TYPE_CHECKING:
  from .user_model import UserModel
  from .user_search_link_model import UserSearchLinkModel

class SearchLinkModel(BaseModel):
  __tablename__ = "search_links"

  id: Mapped[int] = mapped_column(
    BigInteger,
    primary_key=True,
    autoincrement=True,
  )

  search_link: Mapped[str] = mapped_column(
    Text,
  )

  _source_name: Mapped[SourceName] = mapped_column(
    "source_name",
    Text,
  )

  @property
  def source_name(self) -> SourceName:
    return SourceName[self._source_name]

  @source_name.setter
  def source_name(self, source: SourceName) -> None:
    self._source_name = source.value

  is_active: Mapped[bool] = mapped_column(
    Boolean,
    server_default=expression.true(),
  )

  name: Mapped[str] = mapped_column(
    String(255),
    nullable=True,
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
