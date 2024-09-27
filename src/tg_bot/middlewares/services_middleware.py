from typing import (
  Callable,
  Dict,
  Any,
  Awaitable,
)
from aiogram import BaseMiddleware
from aiogram.types import Message
from src.shared import db_service
from src.api.users_telegrams.user_telegram_service import UserTelegramService
from src.api.users.user_service import UserService
from src.api.search_links.search_link_service import SearchLinkService
from src.api.parsing_results.parsing_result_service import ParsingResultService

class ServicesMiddleware(BaseMiddleware):
  async def __call__(
    self,
    handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
    event: Message,
    data: Dict[str, Any],
  ) -> Any:
    async with db_service.session_factory() as session:
      user_telegram_service = UserTelegramService(session=session)
      user_service = UserService(session=session)
      search_link_service = SearchLinkService(session=session)
      parsing_result_service = ParsingResultService(session=session)

      data["user_telegram_service"] = user_telegram_service
      data["user_service"] = user_service
      data["search_link_service"] = search_link_service
      data["parsing_result_service"] = parsing_result_service

      result = await handler(event, data)

      return result
