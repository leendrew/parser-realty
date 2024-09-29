from uuid import UUID
from typing import (
  Annotated,
  Sequence,
)
from fastapi import Depends
from sqlalchemy import (
  select,
  update,
  delete,
  func,
)
from src.shared import (
  Logger,
  BaseService,
)
from src.utils.link_validator import LinkValidator
from src.models.search_link_model import SearchLinkModel
from src.models.user_model import UserModel
from .search_link_types import (
  SourceName,
  SearchType,
)

logger = Logger().get_instance()

MAX_USER_LINKS_COUNT = 5

class SearchLinkService(BaseService):
  async def create_one_to_user(
    self,
    search_type: SearchType,
    link: str,
    source_name: SourceName,
    name: str,
    user: UserModel,
  ) -> SearchLinkModel:
    is_link_https = LinkValidator.is_valid_https(link)
    if not is_link_https:
      message = "Невалидный протокол"
      logger.error(f"{message} у ссылки \"{link}\"")
      raise Exception(message)

    is_valid_source_link = LinkValidator.is_valid_source(
      source=source_name,
      link=link
    )
    if not is_valid_source_link:
      logger.error(f"Ссылки с сайта \"{source_name.value}\" не поддерживаются")
      raise Exception("Ссылки данного сайте не поддерживаются")
    
    stmt = (
      select(func.count())
      .join(SearchLinkModel.users)
      .where(UserModel.id == user.id)
    )

    user_search_links_count = await self.session.scalar(stmt)
    if user_search_links_count >= MAX_USER_LINKS_COUNT:
      message = "Превышено допустимое количество ссылок"
      logger.error(f"{message} для пользователя с id \"{user.id}\"")
      raise Exception(message)

    model = SearchLinkModel(
      search_type=search_type.value,
      search_link=link,
      source_name=source_name.value,
      name=name,
      is_active=True,
    )
    model.users.append(user)

    try:
      self.session.add(model)
      await self.session.commit()
      await self.session.refresh(model)

      return model

    except Exception:
      await self.session.rollback()

      message = "Ошибка при сохранении ссылки"
      logger.exception(f"{message} \"{link}\" для пользователя с id \"{user.id}\"")
      raise Exception(message)

  async def get_all_by(
    self,
    id: int | None = None,
    search_type: SearchType | None = None,
    source_name: SourceName | None = None,
    is_active: bool | None = None,
    user_id: UUID | None = None,
  ) -> Sequence[SearchLinkModel]:
    stmt = (
      select(SearchLinkModel)
      .join(SearchLinkModel.users)
    )

    filters = []
    if id is not None:
      filters.append(SearchLinkModel.id == id)
    if search_type is not None:
      filters.append(SearchLinkModel.search_type == search_type.value)
    if source_name is not None:
      filters.append(SearchLinkModel.source_name == source_name.value)
    if is_active is not None:
      filters.append(SearchLinkModel.is_active == is_active)
    if user_id is not None:
      filters.append(UserModel.id == user_id)

    if filters:
      stmt = stmt.filter(*filters)

    links = await self.session.scalars(stmt)

    return links.all()

  async def edit_one(
    self,
    id: int,
    is_active: bool,
  ) -> SearchLinkModel:
    stmt = (
      update(SearchLinkModel)
      .where(SearchLinkModel.id == id)
      .values(is_active=is_active)
      .returning(SearchLinkModel)
    )

    try:
      model = await self.session.scalar(stmt)

      return model

    except Exception:
      await self.session.rollback()

      message = "Ошибка при обновлении ссылки"
      logger.exception(f"{message} с id \"{id}\"")
      raise Exception(message)

  async def delete_one(
    self,
    id: int,
  ) -> SearchLinkModel | None:
    stmt = (
      delete(SearchLinkModel)
      .where(SearchLinkModel.id == id)
      .returning(SearchLinkModel)
    )

    try:
      model = await self.session.scalar(stmt)
      await self.session.commit()

      return model

    except Exception:
      await self.session.rollback()

      message = "Ошибка при удалении ссылки"
      logger.exception(f"{message} с id \"{id}\"")
      raise Exception(message)

SearchLinkServiceDependency = Annotated[SearchLinkService, Depends()]
