from typing import TYPE_CHECKING
from uuid import UUID
from sqlalchemy import func
from sqlalchemy.orm import (
  mapped_column,
  relationship,
  Mapped,
)
from .base_model import BaseModel
if TYPE_CHECKING:
  from .search_link_model import SearchLinkModel
  from .user_search_link_model import UserSearchLinkModel
  from .user_telegram_model import UserTelegramModel

class UserModel(BaseModel):
  __tablename__ = "users"

  id: Mapped[UUID] = mapped_column(
    primary_key=True,
    server_default=func.gen_random_uuid(),
  )

  # m2m
  search_links: Mapped[list["SearchLinkModel"]] = relationship(
    back_populates="users",
    secondary="users_search_links",
  )
  # o2m
  user_users_search_links_associations: Mapped[list["UserSearchLinkModel"]] = relationship(
    back_populates="user",
    viewonly=True,
  )
  # o2o
  telegram: Mapped["UserTelegramModel"] = relationship(
    back_populates="user",
  )
