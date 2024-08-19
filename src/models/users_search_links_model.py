from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy.orm import (
  mapped_column,
  relationship,
  Mapped,
)
from sqlalchemy import (
  ForeignKey,
  UUID as PSQL_UUID,
  Integer,
  BigInteger,
)
from .base_model import BaseModel
if TYPE_CHECKING:
  from . import UsersModel
  from . import SearchLinksModel
  from . import ParsingResultsModel

class UsersSearchLinks(BaseModel):
  id: Mapped[int] = mapped_column(
    BigInteger,
    primary_key=True,
    autoincrement=True,
  )

  user_id: Mapped[UUID] = mapped_column(
    PSQL_UUID,
    ForeignKey(
      "users.id",
      ondelete="CASCADE",
    ),
  )
  # m2o
  user: Mapped["UsersModel"] = relationship(
    back_populates="user_search_links",
  )

  search_link_id: Mapped[int] = mapped_column(
    Integer,
    ForeignKey(
      "search_links.id",
      ondelete="CASCADE",
    ),
  )
  # m2o
  search_link: Mapped["SearchLinksModel"] = relationship(
    back_populates="user_search_links",
  )

  # o2m
  parsing_results: Mapped[list["ParsingResultsModel"]] = relationship(
    back_populates="user_search_link",
    cascade="all, delete-orphan",
  )
