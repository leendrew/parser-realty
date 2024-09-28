from typing import Annotated
from fastapi import Depends
from src.shared import (
  Logger,
  Fetcher,
  queues,
)
from .parser_avito import ParserAvito
from .parser_yandex import ParserYandex
from .parser_cian import ParserCian
from src.api.parsing_results.parsing_result_types import ParsingResult
from src.api.search_links.search_link_types import SourceName

logger = Logger().get_instance()

class ParsingService:
  def __init__(self) -> None:
    self.fetcher = Fetcher()
    self.parser_avito = ParserAvito()
    self.parser_yandex = ParserYandex()
    self.parser_cian = ParserCian()

  async def dispatcher(
    self,
    source: SourceName,
    link: str,
  ) -> None:
    queue_index_by_source = {
      SourceName.avito: 0,
      SourceName.yandex: 1,
      SourceName.cian: 2,
    }

    queue_index = queue_index_by_source[source]
    if queue_index is None:
      logger.error(f"Вы дэбил. {source} {queue_index}")

    task = await queues.add_task(
      queue_index=queue_index,
      fn=self.parse_and_proceed,
      source=source,
      link=link,
    )
    await task
    result = task.result()

    return result

  async def parse_and_proceed(
    self,
    source: SourceName,
    link: str,
  ):
    # result = await self.parse(
    #   source=source,
    #   link=link,
    # )
    result = await self.parse_test(source=source)

    # save result

    return result

  async def parse(
    self,
    source: SourceName,
    link: str,
  ) -> list[ParsingResult]:
    method_by_source = {
      SourceName.avito: self.parser_avito.parse,
      SourceName.yandex: self.parser_yandex.parse,
      SourceName.cian: self.parser_cian.parse,
    }

    method = method_by_source[source]
    if not method:
      message = f"Для источника \"{source}\" не нашлось парсера"
      logger.error(message)
      raise Exception(message)

    fetch_response = await self.fetcher.get_with_retry(url=link)
    bytes_response = fetch_response.content

    result = await method(markup=bytes_response)

    return result

  async def parse_test(
    self,
    source: SourceName,
  ) -> list[ParsingResult]:
    method_by_source = {
      SourceName.avito: self.parser_avito.parse,
      SourceName.yandex: self.parser_yandex.parse,
      SourceName.cian: self.parser_cian.parse,
    }

    method = method_by_source[source]
    if not method:
      message = f"Для источника \"{source}\" не нашлось парсера"
      logger.error(message)
      raise Exception(message)

    filename_by_source = {
      SourceName.avito: "avito-flat",
      # SourceName.avito: "avito-room",
      # SourceName.avito: "avito-house",
      SourceName.yandex: "yandex-flat",
      # SourceName.yandex: "yandex-room",
      # SourceName.yandex: "yandex-house",
      SourceName.cian: "cian-flat",
    }

    filename = f"{filename_by_source[source]}.html"
    folder_name = "test_data"

    import os
    path = os.path.join(folder_name, filename)
    if path is None:
      message = f"Для источника \"{source}\" не нашлось тестового файла"
      logger.error(message)
      raise Exception(message)

    with open(file=path, mode="r") as file:
      content = file.read()
      result = await method(markup=content)

      return result

ParsingServiceDependency = Annotated[ParsingService, Depends()]
