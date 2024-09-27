from aiogram import (
  Bot as AiogramBot,
  Dispatcher,
)
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommandScopeAllPrivateChats
from src.shared import Logger
from src.config import config
from .middlewares.services_middleware import ServicesMiddleware
from .callbacks import callbacks_routers
from .commands import (
  commands_routers,
  ui_commands,
)

routers = [*callbacks_routers, *commands_routers]

logger = Logger().get_instance()

dp = Dispatcher()
dp.update.middleware(ServicesMiddleware())
dp.include_routers(*routers)

class Bot:
  def __init__(self) -> None:
    self.__instance = AiogramBot(
      token=config.tg.botapikey,
      default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

  async def start(self) -> None:
    await self.__instance.set_my_commands(
      commands=ui_commands,
      scope=BotCommandScopeAllPrivateChats(),
    )
    await dp.start_polling(self.__instance)

  async def stop(self) -> None:
    await dp.stop_polling(self.__instance)
    await self.__instance.session.close()
