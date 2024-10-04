from uuid import UUID
from typing import (
  Annotated,
  Sequence,
)
from fastapi import Depends
from sqlalchemy import (
  select,
)
from aiogram.utils import markdown
from src.shared import (
  Logger,
  BaseService,
)
from src.models.user_telegram_model import UserTelegramModel
from src.models.parsing_result_model import ParsingResultModel

logger = Logger().get_instance()

# ! FIX: extracting this cause cycle import
def get_my_link_parsing_result_message(parsing_results: list[ParsingResultModel]) -> list[str]:
  no_value_text = "не указано"

  texts = []
  for index, parsing_result in enumerate(parsing_results):
    number = index + 1
    deposit_percent = parsing_result.deposit_percent
    commission_percent = parsing_result.commission_percent

    price_text = f"Цена – {parsing_result.price}"
    deposit_value_text = deposit_percent if deposit_percent is not None else no_value_text
    deposit_text = f"Залог – {deposit_value_text}"
    commission_value_text = commission_percent if commission_percent is not None else no_value_text
    commission_text = f"Комиссия – {commission_value_text}"

    values_text = ". ".join([number, price_text, deposit_text, commission_text])
    link_text = f"Ссылка – {parsing_result.direct_link}"
    texts.append(values_text)
    texts.append(link_text)

  return texts

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

  async def get_one_by_user_id(
    self,
    user_id: UUID,
  ) -> UserTelegramModel | None:
    stmt = (
      select(UserTelegramModel)
      .where(UserTelegramModel.user_id == user_id)
    )

    telegram_user = await self.session.scalar(stmt)

    return telegram_user

  async def notify_telegram_user(
    self,
    user_telegram_id: int,
    link_name: str,
    parsing_results: list[ParsingResultModel],
  ) -> None:
    try:
      from src.tg_bot.bot import tg_bot

      title_text = f"Ваш результат для ссылки \"{link_name}\":"
      texts = get_my_link_parsing_result_message(parsing_results=parsing_results)

      text = markdown.text(
        title_text,
        *texts,
        sep="\n",
      )
      await tg_bot.send_message(
        chat_id=user_telegram_id,
        text=text,
        disable_web_page_preview=True,
      )

    except Exception:
      logger.exception("User Telegram Service")

UserTelegramServiceDependency = Annotated[UserTelegramService, Depends()]
