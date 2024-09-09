from typing import Annotated
from fastapi import Depends
from src.shared import (
  Fetcher,
  Logger,
)
from .parser_avito import ParserAvito
from .parser_yandex import ParserYandex
from .parser_cian import ParserCian
from src.api.parsing_results.parsing_result_types import ParsingResult
from src.api.search_links.search_link_types import SourceName
from src.api.parsing_results.parsing_result_types import HousingType

logger = Logger().get_instance()

class ParsingService:
  def __init__(self) -> None:
    self.fetcher = Fetcher()
    self.parser_avito = ParserAvito()
    self.parser_yandex = ParserYandex()
    self.parser_cian = ParserCian()

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

    fetch_response = self.fetcher.get_with_retry(url=link)
    bytes_response = fetch_response.content

    result = await method(markup=bytes_response)

    return result

ParsingServiceDependency = Annotated[ParsingService, Depends()]
