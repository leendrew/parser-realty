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
  from .parsing_result_model import ParsingResultModel
  from .user_model import UserModel
  from .search_link_model import SearchLinkModel

class UserSearchLinkModel(BaseModel):
  __tablename__ = "users_search_links"

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
  user: Mapped["UserModel"] = relationship(
    back_populates="user_users_search_links_associations",
    viewonly=True,
  )

  search_link_id: Mapped[int] = mapped_column(
    Integer,
    ForeignKey(
      "search_links.id",
      ondelete="CASCADE",
    ),
    index=True,
    unique=True,
  )
  # m2o
  search_link: Mapped["SearchLinkModel"] = relationship(
    back_populates="search_link_users_search_links_associations",
    viewonly=True,
  )

  # o2m
  parsing_results: Mapped[list["ParsingResultModel"]] = relationship(
    back_populates="user_search_link",
    cascade="all, delete-orphan",
  )
