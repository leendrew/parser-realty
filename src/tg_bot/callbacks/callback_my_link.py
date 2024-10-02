from aiogram import (
  Router,
  F,
)
from aiogram.utils import markdown
from aiogram.types import (
  CallbackQuery,
  Message,
)
from aiogram.fsm.context import FSMContext
from src.shared import Logger
from .callback_types import (
  MyLinkCallbackData,
  MyLinkCallbackPayload,
)
from .callback_states import MyLinkState
from ..keyboards.keyboard_types import KeyboardMyLinkKey
from ..keyboards.keyboard_my_link import (
  get_my_link_keyboard,
  get_my_link_delete_keyboard,
  get_my_link_reset_keyboard,
)
from ..keyboards.keyboard_menu import get_menu_keyboard
from ..shared import (
  get_my_link_message,
  supported_sources_text,
)
from ..utils import remove_last_bot_message_reply_markup
from src.api.search_links.search_link_service import SearchLinkService
from src.utils.link_validator import LinkValidator

from src.api.search_links.search_link_types import SearchType

logger = Logger().get_instance()

router = Router()

@router.callback_query(MyLinkCallbackData.filter(F.action == KeyboardMyLinkKey.home))
async def on_my_link_home_callback_handler(
  cb_query: CallbackQuery,
  callback_data: MyLinkCallbackData,
  state: FSMContext,
) -> None:
  await cb_query.answer()
  await state.update_data(id=callback_data.id)

  link = MyLinkCallbackPayload(**callback_data.model_dump(exclude=["action"]))

  keyboard = get_my_link_keyboard(
    link=link,
  )
  text = markdown.text(
    "Ваша ссылка:",
    *get_my_link_message(link=link),
    sep="\n",
  )
  await cb_query.message.edit_text(
    text=text,
    reply_markup=keyboard,
  )

@router.callback_query(MyLinkCallbackData.filter(F.action == KeyboardMyLinkKey.edit_name))
async def on_my_link_edit_name_callback_handler(
  cb_query: CallbackQuery,
  callback_data: MyLinkCallbackData,
  state: FSMContext,
) -> None:
  await cb_query.answer()
  await state.update_data(last_bot_message_id=cb_query.message.message_id)
  await state.update_data(search_link=callback_data.name)
  await state.set_state(MyLinkState.name)

  keyboard = get_my_link_reset_keyboard()
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
  MyLinkState.name,
  F.text
)
async def on_my_link_edit_name_correct_callback_handler(
  message: Message,
  state: FSMContext,
  search_link_service: SearchLinkService,
) -> None:
  name = message.text

  data = await state.get_data()

  try:
    updated_link = await search_link_service.edit_one(
      id=data["id"],
      name=name,
    )
    if not updated_link:
      raise ValueError()

    link_data = MyLinkCallbackPayload.model_validate(updated_link)

    await remove_last_bot_message_reply_markup(
      message=message,
      state=state,
    )
    await state.clear()

    keyboard = get_my_link_keyboard(link=link_data)
    text = markdown.text(
      "Ваша ссылка обновлена:",
      *get_my_link_message(link=link_data),
      sep="\n",
    )
    await message.answer(
      text=text,
      reply_markup=keyboard,
    )

  except Exception:
    logger.exception("Update SearchLink name")
    text = markdown.text(
      "Произошла ошибка, попробуйте снова",
      sep="\n",
    )
    await message.answer(
      text=text,
    )

@router.message(MyLinkState.name)
async def on_my_link_edit_name_incorrect_callback_handler(message: Message) -> None:
  text = markdown.text(
    "Ошибка! Я просил ввести текст",
    "Попробуйте еще раз",
    sep="\n",
  )
  await message.answer(
    text=text,
  )

@router.callback_query(MyLinkCallbackData.filter(F.action == KeyboardMyLinkKey.edit_link))
async def on_my_link_edit_link_callback_handler(
  cb_query: CallbackQuery,
  state: FSMContext,
) -> None:
  await cb_query.answer()
  await state.update_data(last_bot_message_id=cb_query.message.message_id)
  await state.set_state(MyLinkState.search_link)

  await remove_last_bot_message_reply_markup(
    message=cb_query.message,
    state=state,
  )

  keyboard = get_my_link_reset_keyboard()
  text = markdown.text(
    "Выберите максимально строгие фильтры",
    "Поставьте сортировку по дате (сначала новые)",
    *supported_sources_text,
    sep="\n",
  )
  sended_message = await cb_query.message.edit_text(
    text=text,
    reply_markup=keyboard,
  )
  await state.update_data(last_bot_message_id=sended_message.message_id)

@router.message(
  MyLinkState.search_link,
  F.text
)
async def on_my_link_edit_link_correct_callback_handler(
  message: Message,
  state: FSMContext,
  search_link_service: SearchLinkService,
) -> None:
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

  link_source = LinkValidator.get_link_source(link=link)
  if not link_source:
    text = markdown.text(
      "Ошибка! Ссылка с данного сайта не поддерживаются",
      *supported_sources_text,
      sep="\n",
    )
    await message.answer(
      text=text,
    )
    return

  try:
    updated_link = await search_link_service.edit_one(
      id=data["id"],
      search_link=link,
    )
    if not updated_link:
      raise ValueError()

    link_data = MyLinkCallbackPayload.model_validate(updated_link)

    await remove_last_bot_message_reply_markup(
      message=message,
      state=state,
    )
    await state.clear()

    keyboard = get_my_link_keyboard(link=link_data)
    text = markdown.text(
      "Ваша ссылка обновлена:",
      *get_my_link_message(link=link_data),
      sep="\n",
    )
    await message.answer(
      text=text,
      reply_markup=keyboard,
    )

  except Exception:
    logger.exception("Update SearchLink search_link")
    text = markdown.text(
      "Произошла ошибка, попробуйте снова",
      sep="\n",
    )
    await message.answer(
      text=text,
    )

@router.message(MyLinkState.search_link)
async def on_my_link_edit_link_incorrect_callback_handler(message: Message) -> None:
  text = markdown.text(
    "Ошибка! Я просил ввести ссылку",
    "Попробуйте еще раз",
    sep="\n",
  )
  await message.answer(
    text=text,
  )

@router.callback_query(MyLinkCallbackData.filter(F.action == KeyboardMyLinkKey.toggle_active))
async def on_my_link_edit_name_callback_handler(
  cb_query: CallbackQuery,
  callback_data: MyLinkCallbackData,
  search_link_service: SearchLinkService,
) -> None:
  await cb_query.answer()

  link = MyLinkCallbackPayload(**callback_data.model_dump(exclude=["action"]))

  try:
    is_active = not link.is_active
    edited_link = await search_link_service.edit_one(
      id=link.id,
      is_active=is_active,
    )
    if not edited_link:
      raise ValueError()

    link = MyLinkCallbackPayload(
      **link.model_dump(exclude=["is_active"]),
      is_active=is_active,
    )

    keyboard = get_my_link_keyboard(link=link)
    text = markdown.text(
      "Ваша ссылка обновлена:",
      *get_my_link_message(link=link),
      sep="\n",
    )
    await cb_query.message.edit_text(
      text=text,
      reply_markup=keyboard,
    )

  except Exception:
    logger.exception("Update SearchLink is_active")
    text = markdown.text(
      "Произошла ошибка, попробуйте снова",
      sep="\n",
    )
    await cb_query.message.answer(
      text=text,
    )

@router.callback_query(MyLinkCallbackData.filter(F.action == KeyboardMyLinkKey.delete_link))
async def on_my_link_edit_name_callback_handler(
  cb_query: CallbackQuery,
  callback_data: MyLinkCallbackData,
) -> None:
  await cb_query.answer()

  link = MyLinkCallbackPayload(**callback_data.model_dump(exclude=["action"]))

  keyboard = get_my_link_delete_keyboard(link=link)
  text = markdown.text(
    "Вы уверены, что хотите удалить ссылку с названием \"" + markdown.hbold(link.name) + "\"",
    sep="\n",
  )
  await cb_query.message.edit_text(
    text=text,
    reply_markup=keyboard,
  )

@router.callback_query(MyLinkCallbackData.filter(F.action == KeyboardMyLinkKey.delete_link_confirm))
async def on_my_link_delete_confirm_callback_handler(
  cb_query: CallbackQuery,
  callback_data: MyLinkCallbackData,
  search_link_service: SearchLinkService,
) -> None:
  await cb_query.answer()

  link = MyLinkCallbackPayload(**callback_data.model_dump(exclude=["action"]))

  try:
    deleted_link = await search_link_service.delete_one(id=link.id)
    if not deleted_link:
      raise ValueError()

    keyboard = get_menu_keyboard()
    text = markdown.text(
      "Ссылка с названием \"" + markdown.hbold(deleted_link.name) + "\" удалена",
      sep="\n",
    )
    await cb_query.message.edit_text(
      text=text,
      reply_markup=keyboard,
    )

  except Exception:
    logger.exception("Delete SearchLink")
    keyboard = get_my_link_delete_keyboard(link=link)
    text = markdown.text(
      "Произошла ошибка, попробуйте снова",
      sep="\n",
    )
    await cb_query.message.edit_text(
      text=text,
      reply_markup=keyboard,
    )

@router.callback_query(
  MyLinkCallbackData.filter(F.action == KeyboardMyLinkKey.reset),
  MyLinkState(),
)
async def on_my_link_edit_reset_callback_handler(
  cb_query: CallbackQuery,
  state: FSMContext,
) -> None:
  await cb_query.answer()
  await state.clear()

  keyboard = get_menu_keyboard()
  text = markdown.text(
    "Изменение ссылки сброшено",
    "Выберите действие:",
    sep="\n",
  )
  await cb_query.message.edit_text(
    text=text,
    reply_markup=keyboard,
  )
