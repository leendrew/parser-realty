from typing import Annotated
from fastapi import (
  Depends,
  HTTPException,
)
from src.shared import (
  Logger,
  BaseService,
)
from src.models.parsing_result_model import ParsingResultModel
from .parsing_result_types import CreateOnePayload

logger = Logger().get_instance()

class ParsingResultService(BaseService):
  async def create_one(
    self,
    payload: CreateOnePayload,
  ) -> ParsingResultModel:
    model = ParsingResultModel(**payload.model_dump())

    try:
      self.session.add(model)
      await self.session.commit()
      await self.session.refresh(model)

      return model

    except Exception:
      message = f"Ошибка при сохранении результата"
      logger.exception(message)
      # TODO: correct status code
      raise HTTPException(
        status_code=400,
        detail=message,
      )

  async def create_many(
    self,
    payload: list[CreateOnePayload],
  ) -> list[ParsingResultModel]:
    models: list[ParsingResultModel] = []
    for data in payload:
      model = ParsingResultModel(**data.model_dump())
      models.append(model)

    try:
      self.session.add_all(models)
      await self.session.commit()
      await self.session.refresh(models)

      return models
    
    except Exception:
      await self.session.rollback()

      message = "Ошибка при сохранении результатов парсинга"
      logger.exception(message)
      # TODO: correct status code
      raise HTTPException(
        status_code=400,
        detail=message,
      )

ParsingResultServiceDependency = Annotated[ParsingResultService, Depends()]
