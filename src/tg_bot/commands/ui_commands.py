from aiogram.types import BotCommand
from .command_types import CommandKey

ui_commands = [
  BotCommand(
    command=CommandKey.start.value,
    description="Старт",
  ),
  BotCommand(
    command=CommandKey.help.value,
    description="Информация",
  ),
  BotCommand(
    command=CommandKey.stop.value,
    description="Стоп",
  ),
  BotCommand(
    command=CommandKey.menu.value,
    description="Меню",
  ),
]
