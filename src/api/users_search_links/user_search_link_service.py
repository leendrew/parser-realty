from uuid import UUID
from typing import (
  Annotated,
  Sequence,
)
from fastapi import Depends
from sqlalchemy import (
  select,
)
from sqlalchemy.orm import joinedload
from src.shared import (
  Logger,
  BaseService,
)
from src.models.user_search_link_model import UserSearchLinkModel
from src.models.search_link_model import SearchLinkModel
from src.api.search_links.search_link_types import SearchType

logger = Logger().get_instance()

class UserSearchLinkService(BaseService):
  async def get_one_by(
    self,
    id: int | None = None,
  ) -> UserSearchLinkModel | None:
    stmt = (
      select(UserSearchLinkModel)
      # .join(UserSearchLinkModel.user)
      # .options(joinedload(UserSearchLinkModel.user))
      .join(UserSearchLinkModel.search_link)
      .options(joinedload(UserSearchLinkModel.search_link))
    )

    filters = []
    if id is not None:
      filters.append(UserSearchLinkModel.id == id)

    if filters:
      stmt = stmt.filter(*filters)

    result = await self.session.scalar(stmt)

    return result

  async def get_all_by(
    self,
    id: int | None = None,
    user_id: UUID | None = None,
    search_link_id: int | None = None,
    search_link_search_type: SearchType | None = None,
    is_link_active: bool | None = None,
  ) -> Sequence[UserSearchLinkModel]:
    stmt = (
      select(UserSearchLinkModel)
      .join(UserSearchLinkModel.user)
      .options(joinedload(UserSearchLinkModel.user))
      .join(UserSearchLinkModel.search_link)
      .options(joinedload(UserSearchLinkModel.search_link))
    )

    filters = []
    if id is not None:
      filters.append(UserSearchLinkModel.id == id)
    if user_id is not None:
      filters.append(UserSearchLinkModel.user_id == user_id)
    if search_link_id is not None:
      filters.append(UserSearchLinkModel.search_link_id == search_link_id)
    if search_link_search_type is not None:
      filters.append(SearchLinkModel.search_type == search_link_search_type.value)
    if is_link_active is not None:
      filters.append(SearchLinkModel.is_active == is_link_active)

    if filters:
      stmt = stmt.filter(*filters)

    result = await self.session.scalars(stmt)

    return result.all()

UserSearchLinkServiceDependency = Annotated[UserSearchLinkService, Depends()]
