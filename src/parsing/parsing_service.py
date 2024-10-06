from typing import Annotated
from asyncio import gather
from fastapi import Depends
from src.shared import (
  Logger,
  Fetcher,
  queues,
)
from .parser_avito import ParserAvito
from .parser_yandex import ParserYandex
from .parser_cian import ParserCian
from src.api.users_search_links.user_search_link_service import UserSearchLinkService
from src.api.parsing_results.parsing_result_service import ParsingResultService
from src.api.users_telegrams.user_telegram_service import UserTelegramService
from src.api.parsing_results.parsing_result_types import ParsingResult
from src.api.search_links.search_link_types import (
  SourceName,
  SearchType,
)
from src.models.parsing_result_model import ParsingResultModel
from src.shared import db_service

import undetected_chromedriver as ucd

logger = Logger().get_instance()

class ParsingService:
  def __init__(self) -> None:
    self.fetcher = Fetcher()
    self.parser_avito = ParserAvito()
    self.parser_yandex = ParserYandex()
    self.parser_cian = ParserCian()
    self.db_service = db_service

  async def dispatch(
    self,
    search_type: SearchType,
  ) -> None:
    async with self.db_service.session_factory() as session:
      user_search_link_service = UserSearchLinkService(session=session)
      parsing_result_service = ParsingResultService(session=session)
      user_telegram_service = UserTelegramService(session=session)

      # TODO: перевыбрасывать все ошибки наверх
      try:
        user_search_links = await user_search_link_service.get_all_by(
          search_link_search_type=search_type,
          is_link_active=True,
        )

        link_results_tasks = []
        for user_search_link in user_search_links:
          task = self.parse_and_proceed(
            source=user_search_link.search_link.source_name,
            link=user_search_link.search_link.search_link,
          )
          link_results_tasks.append(task)

        link_results: list[list[ParsingResult]] = await gather(*link_results_tasks)

        parsing_results_tasks = []
        for (index, link_result) in enumerate(link_results):
          user_search_link = user_search_links[index]

          task = parsing_result_service.create_unique(
            payload=link_result,
            user_search_link=user_search_link,
          )
          parsing_results_tasks.append(task)

        new_parsing_results: list[list[ParsingResultModel]] = await gather(*parsing_results_tasks)

        notify_telegram_users_tasks = []
        for new_results in new_parsing_results:
          if not new_results:
            continue

          new_result_first = new_results[0]
          user_search_link = await user_search_link_service.get_one_by(id=new_result_first.user_search_link_id)
          telegram_user = await user_telegram_service.get_one_by_user_id(user_id=user_search_link.user_id)

          task = user_telegram_service.notify_telegram_user(
            user_telegram_id=telegram_user.telegram_id,
            link_name=user_search_link.search_link.name,
            parsing_results=new_results,
          )
          notify_telegram_users_tasks.append(task)

        await gather(*notify_telegram_users_tasks)

      except Exception:
        logger.exception("@@@ Пизда")

  async def parse_and_proceed(
    self,
    source: str,
    link: str,
  ) -> list[ParsingResult]:
    queue_index_by_source = {
      SourceName.avito.value: 0,
      SourceName.yandex.value: 1,
      SourceName.cian.value: 2,
    }

    queue_index = queue_index_by_source[source]
    if queue_index is None:
      message = "Вы дэбил"
      logger.error(f"{message} {source} {queue_index}")
      raise IndexError(message)

    try:
      task = await queues.add_task(
        queue_index=queue_index,
        fn=self.parse,
        source=source,
        link=link,
      )
      await task
      result = task.result()

      return result

    except Exception:
      logger.exception("Parse and Proceed")

      task.cancel()
      return []

  async def parse(
    self,
    source: str,
    link: str,
  ) -> list[ParsingResult]:
    method_by_source = {
      SourceName.avito.value: self.parser_avito.parse,
      SourceName.yandex.value: self.parser_yandex.parse,
      SourceName.cian.value: self.parser_cian.parse,
    }

    method = method_by_source[source]
    if not method:
      message = f"Для источника \"{source}\" не нашлось парсера"
      logger.error(message)
      raise ValueError(message)

    try:
      d = ucd.Chrome()
      d.get(link)
      d.save_screenshot()
      bytes_response = d.page_source
      # fetch_response = await self.fetcher.get_with_retry(url=link)
      # bytes_response = fetch_response.content

      result = await method(markup=bytes_response)

      return result

    except Exception:
      logger.exception("Parse")
      return []

ParsingServiceDependency = Annotated[ParsingService, Depends()]
