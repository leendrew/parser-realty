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
from src.api.search_links.search_link_types import SourceName
from .base_model import BaseModel
if TYPE_CHECKING:
  from .user_model import UserModel

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

  source_name: Mapped[SourceName] = mapped_column(
    Text,
  )

  # m2m
  users: Mapped[list["UserModel"]] = relationship(
    back_populates="search_links",
    secondary="users_search_links",
  )
