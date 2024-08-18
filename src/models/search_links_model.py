from typing import TYPE_CHECKING
from sqlalchemy.orm import (
  mapped_column,
  relationship,
  Mapped,
)
from sqlalchemy import (
  BigInteger,
  Text,
)
from src.api.search_links.search_links_types import SourceName
from .base_model import BaseModel
if TYPE_CHECKING:
  from . import UsersModel
  from . import UsersSearchLinksModel

class SearchLinks(BaseModel):
  id: Mapped[int] = mapped_column(
    BigInteger,
    primary_key=True,
    autoincrement=True,
  )

  search_link: Mapped[str] = mapped_column(
    Text,
  )

  source_name: Mapped[SourceName] = mapped_column(
    Text,
  )

  # m2m
  users: Mapped[list["UsersModel"]] = relationship(
    back_populates="search_links",
    secondary="users_search_links",
  )

  # o2m
  user_search_link: Mapped[list["UsersSearchLinksModel"]] = relationship(
    back_populates="search_link",
  )
