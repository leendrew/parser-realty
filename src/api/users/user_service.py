from uuid import UUID
from typing import (
  Annotated,
  Sequence,
)
from asyncio import gather
from fastapi import Depends
from sqlalchemy import (
  select,
  delete,
  func,
)
from src.shared import (
  Logger,
  BaseService,
)
from src.models.user_model import UserModel
from src.models.user_search_link_model import UserSearchLinkModel
from src.models.search_link_model import SearchLinkModel
from src.models.parsing_result_model import ParsingResultModel
from .user_types import UserSummary

logger = Logger().get_instance()

class UserService(BaseService):
  async def create_one(self) -> UserModel:
    model = UserModel()
    try:
      self.session.add(model)
      await self.session.commit()
      await self.session.refresh(model)

      return model

    except Exception:
      await self.session.rollback()

      message = "Ошибка при создании пользователя"
      logger.exception(message)
      raise Exception(message)

  async def get_all(self) -> Sequence[UserModel]:
    stmt = select(UserModel)
    users = await self.session.scalars(stmt)

    return users.all()

  async def get_one(
    self,
    id: UUID,
  ) -> UserModel | None:
    stmt = (
      select(UserModel)
      .where(UserModel.id == id)
    )

    user = await self.session.scalar(stmt)

    return user
  
  async def delete_one(
    self,
    id: UUID,
  ) -> UserModel | None:
    stmt = (
      delete(UserModel)
      .where(UserModel.id == id)
      .returning(UserModel)
    )

    try:
      result = await self.session.scalar(stmt)
      await self.session.commit()

      return result

    except Exception:
      await self.session.rollback()

      message = "Ошибка при удалении пользователя"
      logger.exception(f"{message} с id \"{id}\"")
      raise Exception(message)
    
  async def get_user_summary(
    self,
    id: UUID,
  ) -> UserSummary:
    user_search_links_count_stmt = (
      select(func.count())
      .join(SearchLinkModel.users)
      .where(UserModel.id == id)
    )

    user_parsing_results_count_stmt = (
      select(func.count())
      .join(UserSearchLinkModel.parsing_results)
      .where(ParsingResultModel.user_search_link_id == UserSearchLinkModel.id)
      .where(UserSearchLinkModel.user_id == id)
    )

    tasks = [
      self.session.scalar(user_search_links_count_stmt),
      self.session.scalar(user_parsing_results_count_stmt),
    ]
    user_search_links_count, user_parsing_results_count = await gather(*tasks)
    result = UserSummary(
      id=id,
      search_links_count=user_search_links_count,
      parsing_results_count=user_parsing_results_count
    )

    return result

UserServiceDependency = Annotated[UserService, Depends()]
