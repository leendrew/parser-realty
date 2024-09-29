from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.utils import markdown
from aiogram.types import Message
from src.shared import Logger
from ..keyboards.keyboard_menu import get_menu_init_keyboard
from src.api.users_telegrams.user_telegram_service import UserTelegramService
from src.api.users.user_service import UserService

logger = Logger().get_instance()

router = Router()

@router.message(CommandStart())
async def on_command_start(
  message: Message,
  user_telegram_service: UserTelegramService,
  user_service: UserService,
) -> None:
  tg_user = message.from_user

  user_telegram = await user_telegram_service.get_one(telegram_id=tg_user.id)
  if user_telegram:
    keyboard = get_menu_init_keyboard()
    text = markdown.text(
      f"Привет, {tg_user.first_name}.",
      "Вы уже в системе",
      sep="\n",
    )

    await message.answer(
      text=text,
      reply_markup=keyboard,
    )
    return

  user = await user_service.create_one()
  await user_telegram_service.create_one(
    telegram_id=tg_user.id,
    user_id=user.id,
  )

  keyboard = get_menu_init_keyboard()
  text = markdown.text(
    f"Привет, {tg_user.full_name}.",
    "Вы добавлены в систему",
    sep="\n",
  )

  await message.answer(
    text=text,
    reply_markup=keyboard,
  )
