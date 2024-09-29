from aiogram import (
  Router,
  F,
)
from aiogram.utils import markdown
from aiogram.types import (
  CallbackQuery,
  Message,
)
from aiogram.fsm.state import (
  StatesGroup,
  State,
)
from aiogram.fsm.context import FSMContext
from src.shared import Logger
from .callback_types import AddLinkCallbackData
from ..keyboards.keyboard_types import KeyboardAddLinkKey
from ..keyboards.keyboard_add_link import (
  get_add_link_source_keyboard,
  get_add_link_process_keyboard,
)
from ..keyboards.keyboard_menu import get_menu_init_keyboard
from src.api.users.user_service import UserService
from src.api.search_links.search_link_service import SearchLinkService
from src.api.search_links.search_link_types import source_name_title_map
from src.utils.link_validator import LinkValidator

logger = Logger().get_instance()

router = Router()

class AddLinkState(StatesGroup):
  last_bot_message_id = State()
  search_type = State()
  source_name = State()
  name = State()
  search_link = State()

async def remove_last_bot_message_reply_markup(
  message: Message,
  state: FSMContext,
) -> None:
  data = await state.get_data()
  await message.bot.edit_message_reply_markup(
    chat_id=message.chat.id,
    message_id=data["last_bot_message_id"],
    reply_markup=None,
  )

@router.callback_query(AddLinkCallbackData.filter(F.action == KeyboardAddLinkKey.home))
async def on_add_link_source_name_handler(
  cb_query: CallbackQuery,
  callback_data: AddLinkCallbackData,
  state: FSMContext,
) -> None:
  logger.info("AddLink SourceName")
  await cb_query.answer()
  tg_user = cb_query.from_user
  await state.update_data(last_bot_message_id=cb_query.message.message_id)
  await state.update_data(search_type=callback_data.search_type)
  await state.set_state(AddLinkState.source_name)

  keyboard = get_add_link_source_keyboard()
  text = markdown.text(
    "Выберите источник",
    sep="\n",
  )
  await cb_query.message.edit_text(
    text=text,
    reply_markup=keyboard,
  )

@router.callback_query(
  AddLinkCallbackData.filter(F.action == KeyboardAddLinkKey.name),
  AddLinkState.source_name,
)
async def on_add_link_name_callback_handler(
  cb_query: CallbackQuery,
  callback_data: AddLinkCallbackData,
  state: FSMContext,
) -> None:
  logger.info("AddLink Name")
  await cb_query.answer()
  await state.update_data(last_bot_message_id=cb_query.message.message_id)
  await state.update_data(source_name=callback_data.source_name)
  await state.set_state(AddLinkState.name)

  keyboard = get_add_link_process_keyboard()
  text = markdown.text(
    "Введите название вашей ссылки",
    "Например, \"однушки рядом с метро\"",
    sep="\n",
  )
  await cb_query.message.edit_text(
    text=text,
    reply_markup=keyboard,
  )

@router.message(
  AddLinkState.name,
  F.text,
)
async def on_add_link_name_correct_handler(
  message: Message,
  state: FSMContext,
) -> None:
  logger.info(f"AddLink Name Correct")
  await state.update_data(name=message.text)
  await state.set_state(AddLinkState.search_link)

  await remove_last_bot_message_reply_markup(
    message=message,
    state=state,
  )

  data = await state.get_data()
  source_name = data["source_name"]
  source_name_title = source_name_title_map[source_name]
  keyboard = get_add_link_process_keyboard()
  text = markdown.text(
    "Выберите максимально строгие фильтры",
    "Если результатов больше, чем на одну страницу, то поставьте сортировку по дате (сначала новые)",
    f"Отправьте ссылку с сайта \"{source_name_title}\"",
    sep="\n",
  )
  sended_message = await message.answer(
    text=text,
    reply_markup=keyboard,
  )
  await state.update_data(last_bot_message_id=sended_message.message_id)

@router.message(AddLinkState.name)
async def on_add_link_name_incorrect_handler(message: Message) -> None:
  logger.info(f"AddLink Name Incorrect")

  text = markdown.text(
    "Ошибка! Я просил ввести текст",
    "Попробуйте еще раз",
    sep="\n",
  )
  await message.answer(
    text=text,
  )

@router.message(
  AddLinkState.search_link,
  F.text,
)
async def on_add_link_search_link_correct_handler(
  message: Message,
  state: FSMContext,
  user_service: UserService,
  search_link_service: SearchLinkService,
) -> None:
  logger.info(f"AddLink SearchLink Correct")
  tg_user = message.from_user

  link = message.text
  data = await state.get_data()

  is_link_has_valid_protocol = LinkValidator.is_valid_https(link=link)
  if not is_link_has_valid_protocol:
    text = markdown.text(
      "Ошибка! Ссылка имеет невалидный протокол",
      "Попробуйте еще раз",
      sep="\n",
    )
    await message.answer(
      text=text,
    )
    return

  is_link_has_valid_source = LinkValidator.is_valid_source(
    link=link,
    source=data["source_name"],
  )
  if not is_link_has_valid_source:
    source_name = data["source_name"]
    source_name_title = source_name_title_map[source_name]
    text = markdown.text(
      f"Ошибка! Ссылка это не ссылка с сайта \"{source_name_title}\"",
      f"Отправьте ссылку с источника \"{source_name_title}\"",
      sep="\n",
    )
    await message.answer(
      text=text,
    )
    return

  user = await user_service.get_one_by_telegram_id(telegram_id=tg_user.id)
  if not user:
    text = markdown.text(
      "Произошла ошибка. Попробуйте снова",
      sep="\n",
    )
    await message.answer(
      text=text,
    )
    return

  created_search_link = await search_link_service.create_one_to_user(
    search_type=data["search_type"],
    link=message.text,
    source_name=data["source_name"],
    name=data["name"],
    user=user,
  )

  await remove_last_bot_message_reply_markup(
    message=message,
    state=state,
  )
  await state.clear()

  keyboard = get_menu_init_keyboard()
  text = markdown.text(
    f"Ссылка с названием {created_search_link.name} создана!",
    sep="\n",
  )
  await message.answer(
    text=text,
    reply_markup=keyboard,
  )

@router.message(AddLinkState.search_link)
async def on_add_link_search_link_incorrect_handler(message: Message) -> None:
  logger.info(f"AddLink SearchLink Incorrect")
  logger.info(message)

  text = markdown.text(
    "Ошибка! Это не ссылка",
    "Попробуйте еще раз",
    sep="\n",
  )
  await message.answer(
    text=text,
  )  

@router.callback_query(
  AddLinkCallbackData.filter(F.action == KeyboardAddLinkKey.reset),
  AddLinkState(),
)
async def on_add_link_reset_handler(
  cb_query: CallbackQuery,
  callback_data: AddLinkCallbackData,
  state: FSMContext,
) -> None:
  logger.info(f"AddLink Reset {callback_data}")
  await cb_query.answer()
  await state.clear()

  keyboard = get_menu_init_keyboard()
  text = markdown.text(
    "Прогресс добавления ссылки сброшен",
    sep="\n",
  )
  await cb_query.message.edit_text(
    text=text,
    reply_markup=keyboard,
  )
