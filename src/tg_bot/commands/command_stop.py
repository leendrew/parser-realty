from aiogram import Router
from aiogram.filters import Command
from aiogram.utils import markdown
from aiogram.types import Message
from src.shared import Logger
from .command_types import CommandKey
from ..keyboards.keyboard_stop import get_stop_keyboard
from src.api.users_telegrams.user_telegram_service import UserTelegramService

logger = Logger().get_instance()

router = Router()

@router.message(Command(CommandKey.stop.value))
async def on_command_stop(
  message: Message,
  user_telegram_service: UserTelegramService,
) -> None:
  tg_user = message.from_user

  telegram_user = await user_telegram_service.get_one(telegram_id=tg_user.id)
  if not telegram_user:
    text = markdown.text(
      "Ошибка! Вас нет в системе",
      "Для начала введите " + markdown.hbold(f"\/{CommandKey.start.value}"),
      sep="\n",
    )

    await message.answer(
      text=text,
    )
    return

  keyboard = get_stop_keyboard(user_id=telegram_user.user_id)
  text = markdown.text(
    "Вы уверены, что хотите удалить все данные?",
    "Их нельзя будет восстановить",
    sep="\n",
  )

  await message.answer(
    text=text,
    reply_markup=keyboard,
  )
