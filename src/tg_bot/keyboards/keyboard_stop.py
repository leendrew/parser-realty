from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from src.shared import Logger
from .keyboard_types import (
  KeyboardStopKey,
)
from ..callbacks.callback_types import (
  StopCallbackData,
)
from src.models.user_telegram_model import UserTelegramModel

logger = Logger().get_instance()

def get_stop_keyboard(telegram_user: UserTelegramModel) -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()
  builder.button(
    text="Удалить",
    callback_data=StopCallbackData(
      action=KeyboardStopKey.confirm,
      user_id=telegram_user.user_id,
    ).pack(),
  )
  builder.button(
    text="Отменить",
    callback_data=StopCallbackData(
      action=KeyboardStopKey.reject,
      user_id=telegram_user.user_id,
    ).pack(),
  )
  builder.adjust(2)

  return builder.as_markup()
