from typing import Annotated
from fastapi import Depends
from sqlalchemy import (
  select,
)
from src.shared import (
  Logger,
  BaseService,
)
from src.models.parsing_result_model import ParsingResultModel
from src.models.user_search_link_model import UserSearchLinkModel
from .parsing_result_types import ParsingResult

logger = Logger().get_instance()

class ParsingResultService(BaseService):
  async def create_one(
    self,
    payload: ParsingResult,
    user_search_link: UserSearchLinkModel
  ) -> ParsingResultModel:
    model = ParsingResultModel(
      **payload.model_dump(),
      user_search_link=user_search_link,
    )

    try:
      self.session.add(model)
      await self.session.commit()
      await self.session.refresh(model)

      return model

    except Exception:
      message = f"Ошибка при сохранении результата"
      logger.exception(message)
      raise Exception(message)

  async def create_many(
    self,
    payload: list[ParsingResult],
    user_search_link: UserSearchLinkModel,
  ) -> list[ParsingResultModel]:
    models: list[ParsingResultModel] = []
    for data in payload:
      model = ParsingResultModel(
        **data.model_dump(),
        user_search_link=user_search_link,
      )
      models.append(model)

    try:
      self.session.add_all(models)
      await self.session.commit()

      return models

    except Exception:
      await self.session.rollback()

      message = "Ошибка при сохранении результатов"
      logger.exception(message)
      raise Exception(message)

  async def get_one(
    self,
    id: int | None = None,
    direct_link: str | None = None,
  ) -> ParsingResultModel | None:
    stmt = (
      select(ParsingResultModel)
    )

    filters = []
    if id is not None:
      filters.append(ParsingResultModel.id == id)
    if direct_link is not None:
      filters.append(ParsingResultModel.direct_link == direct_link)

    stmt = stmt.filter(*filters)

    parsing_result = await self.session.scalar(stmt)

    return parsing_result

  async def create_unique(
    self,
    payload: list[ParsingResult],
    user_search_link: UserSearchLinkModel,
  ) -> list[ParsingResultModel]:
    new_parsing_results = []
    for candidate in payload:
      is_exist = await self.get_one(direct_link=candidate.direct_link)
      if is_exist is None:
        new_parsing_results.append(candidate)

    if not new_parsing_results:
      return []

    try:
      result = await self.create_many(
        payload=new_parsing_results,
        user_search_link=user_search_link,
      )

      return result

    except Exception:
      logger.exception("Create Unique")

      return []

ParsingResultServiceDependency = Annotated[ParsingResultService, Depends()]
