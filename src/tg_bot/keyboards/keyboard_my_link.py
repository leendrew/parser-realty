from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from .keyboard_types import (
  KeyboardMenuKey,
  KeyboardMyLinkKey,
)
from ..callbacks.callback_types import (
  MenuCallbackData,
  MyLinkCallbackData,
)
from src.models.search_link_model import SearchLinkModel

def get_my_link_keyboard(link: SearchLinkModel) -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()
  builder.button(
    text="Изменить ссылку",
    callback_data=MyLinkCallbackData(
      action=KeyboardMyLinkKey.edit_link,
      payload=link,
    ).pack(),
  )
  builder.button(
    text="Изменить название",
    callback_data=MyLinkCallbackData(
      action=KeyboardMyLinkKey.edit_name,
      payload=link,
    ).pack(),
  )
  toggle_active_text = "Деактивировать" if link.is_active else "Активировать"
  builder.button(
    text=toggle_active_text,
    callback_data=MyLinkCallbackData(
      action=KeyboardMyLinkKey.toggle_active,
      payload=link,
    ).pack(),
  )
  builder.button(
    text="Удалить ссылку",
    callback_data=MyLinkCallbackData(
      action=KeyboardMyLinkKey.delete_link,
      payload=link,
    ).pack(),
  )
  builder.button(
    text="Назад",
    callback_data=MenuCallbackData(
      action=KeyboardMenuKey.my_links,
    ).pack(),
  )
  builder.adjust(2)

  return builder.as_markup()
