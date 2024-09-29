from uuid import UUID
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .keyboard_types import (
  KeyboardStopKey,
)
from ..callbacks.callback_types import (
  StopCallbackData,
)

def get_stop_keyboard(user_id: UUID) -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()
  builder.button(
    text="Удалить",
    callback_data=StopCallbackData(
      action=KeyboardStopKey.confirm,
      user_id=user_id,
    ).pack(),
  )
  builder.button(
    text="Отменить",
    callback_data=StopCallbackData(
      action=KeyboardStopKey.reject,
      user_id=user_id,
    ).pack(),
  )
  builder.adjust(2)

  return builder.as_markup()
