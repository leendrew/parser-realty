from asyncio import sleep
from aiogram import Router, F
from aiogram.utils import markdown
from aiogram.types import CallbackQuery
from src.shared import Logger
from .callback_types import StopCallbackData
from src.api.users.user_service import UserService

logger = Logger().get_instance()

router = Router()

@router.callback_query(StopCallbackData.filter())
async def stop_callback_handler(
  cb_query: CallbackQuery,
  callback_data: StopCallbackData,
  user_service: UserService,
) -> None:
  logger.info(f"StopCallbackData {callback_data}")
  await cb_query.answer()
  tg_user = cb_query.from_user

  await cb_query.message.edit_text("Загрузка...")
  await sleep(5)
  await cb_query.message.edit_text("Загрузка завершена")

  # deleted_user = await user_service.delete_one(id=callback_data.payload.telegram_user.user_id)
  # if not deleted_user:
  #   keyboard = ... # TODO
  #   text = markdown.text(
  #     "Произошла ошибка, попробуйте снова",
  #     sep="\n",
  #   )

  #   await cb_query.message.edit_text(
  #     text=text,
  #   )
  #   await cb_query.message.edit_reply_markup(
  #     reply_markup=keyboard,
  #   )
  #   return

  # text = markdown.text(
  #   "Вы удалены из системы. Краткая статистика:",
  #   "Краткая статистика:",
  #   f"id - {deleted_user.id}",
  #   # TODO: перед удалением получать мини стату для юзера, мб без
  #   # f"Количество ссылок - {1}",
  #   # f"Количество результатов парсинга - {1}",
  #   sep="\n",
  # )

  # await message.answer(
  #   text=text,
  # )
