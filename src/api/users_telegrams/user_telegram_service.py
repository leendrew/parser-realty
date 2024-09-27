from uuid import UUID
from typing import (
  Annotated,
  Sequence,
)
from fastapi import Depends
from sqlalchemy import (
  select,
)
from src.shared import (
  Logger,
  BaseService,
)
from src.models.user_telegram_model import UserTelegramModel

logger = Logger().get_instance()

class UserTelegramService(BaseService):
  async def create_one(
    self,
    telegram_id: int,
    user_id: UUID,
  ) -> UserTelegramModel:
    model = UserTelegramModel(
      telegram_id=telegram_id,
      user_id=user_id,
    )

    try:
      self.session.add(model)
      await self.session.commit()
      await self.session.refresh(model)

      return model

    except Exception:
      await self.session.rollback()

      message = "Ошибка при создании телеграма"
      logger.exception(f"{message} для пользователя с id \"{user_id}\" с telegram_id \"{telegram_id}\"")
      raise Exception(message)

  async def get_one(
    self,
    telegram_id: int,
  ) -> UserTelegramModel | None:
    stmt = (
      select(UserTelegramModel)
      .where(UserTelegramModel.telegram_id == telegram_id)
    )

    telegram_user = await self.session.scalar(stmt)

    return telegram_user

UserTelegramServiceDependency = Annotated[UserTelegramService, Depends()]
