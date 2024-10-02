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

def get_my_link_keyboard(link: MyLinkCallbackData) -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()

  edit_name_text = "Изменить название"
  edit_link_text = "Изменить ссылку"
  toggle_active_text = "Деактивировать" if link.is_active else "Активировать"
  delete_link_text = "Удалить ссылку"

  data = [
    (edit_name_text, KeyboardMyLinkKey.edit_name),
    (edit_link_text, KeyboardMyLinkKey.edit_link),
    (toggle_active_text, KeyboardMyLinkKey.toggle_active),
    (delete_link_text, KeyboardMyLinkKey.delete_link),
  ]

  for text, action in data:
    builder.button(
      text=text,
      callback_data=MyLinkCallbackData(
        action=action,
        id=link.id,
        search_type=link.search_type,
        name=link.name,
        source_name=link.source_name,
        is_active=link.is_active,
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

def get_my_link_delete_keyboard(link: MyLinkCallbackData) -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()

  builder.button(
    text="Удалить",
    callback_data=MyLinkCallbackData(
      action=KeyboardMyLinkKey.delete_link_confirm,
      id=link.id,
      search_type=link.search_type,
      name=link.name,
      source_name=link.source_name,
    ).pack(),
  )
  builder.button(
    text="Отменить",
    callback_data=MyLinkCallbackData(
      action=KeyboardMyLinkKey.home,
      id=link.id,
      search_type=link.search_type,
      name=link.name,
      source_name=link.source_name,
      is_active=link.is_active,
    ).pack(),
  )
  builder.adjust(2)

  return builder.as_markup()

def get_my_link_reset_keyboard() -> InlineKeyboardMarkup:
  builder = InlineKeyboardBuilder()

  builder.button(
    text="Сбросить",
    callback_data=MyLinkCallbackData(
      action=KeyboardMyLinkKey.reset,
    ).pack(),
  )
  builder.adjust(1)

  return builder.as_markup()
