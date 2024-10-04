from aiogram import (
  Router,
  F,
)
from aiogram.utils import markdown
from aiogram.types import CallbackQuery
from src.shared import Logger
from .callback_types import MenuCallbackData
from ..keyboards.keyboard_types import KeyboardMenuKey
from ..keyboards.keyboard_menu import (
  get_menu_keyboard,
  get_my_links_keyboard,
  get_no_links_keyboard,
  get_max_links_keyboard,
  get_add_link_search_type_keyboard,
)
from src.api.users_telegrams.user_telegram_service import UserTelegramService
from src.api.search_links.search_link_service import (
  SearchLinkService,
  MAX_USER_LINKS_COUNT,
)
from src.api.search_links.search_link_types import (
  SearchType,
  search_type_title_map,
)


logger = Logger().get_instance()

router = Router()

# ! FIX: extracting this cause cycle import
interval_text_map = {
  SearchType.rent: "каждые 30 минут",
  SearchType.purchase: "каждый день",
}

def __get_search_types_intervals_text() -> list[str]:
  title_text = "Уведомления о новых результатах будут приходить:",
  search_types_intervals = []
  search_types_intervals.append(title_text)

  for search_type in SearchType:
    title = search_type_title_map[search_type]
    interval_text = interval_text_map[search_type]
    text = f"– {title} - {interval_text}"
    search_types_intervals.append(text)

  return search_types_intervals

search_types_intervals_text = __get_search_types_intervals_text()

@router.callback_query(MenuCallbackData.filter(F.action == KeyboardMenuKey.home))
async def on_menu_home_callback_handler(cb_query: CallbackQuery) -> None:
  await cb_query.answer()

  keyboard = get_menu_keyboard()
  text = markdown.text(
    "Это типо меню",
    "Выберите действие",
    sep="\n",
  )
  await cb_query.message.edit_text(
    text=text,
    reply_markup=keyboard,
  )

@router.callback_query(MenuCallbackData.filter(F.action == KeyboardMenuKey.my_links))
async def on_menu_my_links_callback_handler(
  cb_query: CallbackQuery,
  user_telegram_service: UserTelegramService,
  search_link_service: SearchLinkService,
) -> None:
  await cb_query.answer()
  tg_user = cb_query.from_user

  telegram_user = await user_telegram_service.get_one(telegram_id=tg_user.id)
  links = await search_link_service.get_all_by(user_id=telegram_user.user_id)
  if not links:
    keyboard = get_no_links_keyboard()
    text = markdown.text(
      "У вас еще нет ссылок",
      sep="\n",
    )
    await cb_query.message.edit_text(
      text=text,
      reply_markup=keyboard,
    )
    return

  keyboard = get_my_links_keyboard(links=links)
  text = markdown.text(
    "Список ваших ссылок:",
    sep="\n",
  )
  await cb_query.message.edit_text(
    text=text,
    reply_markup=keyboard,
  )

@router.callback_query(MenuCallbackData.filter(F.action == KeyboardMenuKey.add_link))
async def on_menu_add_link_callback_handler(
  cb_query: CallbackQuery,
  user_telegram_service: UserTelegramService,
  search_link_service: SearchLinkService,
) -> None:
  await cb_query.answer()
  tg_user = cb_query.from_user

  telegram_user = await user_telegram_service.get_one(telegram_id=tg_user.id)
  user_links_count = await search_link_service.get_user_links_count(user_id=telegram_user.user_id)
  if user_links_count >= MAX_USER_LINKS_COUNT:
    keyboard = get_max_links_keyboard()
    text = markdown.text(
      "Превышено допустимое количество ссылок",
      "Удалите одну из существующих",
      sep="\n",
    )
    await cb_query.message.edit_text(
      text=text,
      reply_markup=keyboard,
    )
    return

  keyboard = get_add_link_search_type_keyboard()
  text = markdown.text(
    "Выберите, что вы ищете",
    *search_types_intervals_text,
    sep="\n",
  )
  await cb_query.message.edit_text(
    text=text,
    reply_markup=keyboard,
  )
