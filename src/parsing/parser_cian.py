import re
from bs4 import (
  ResultSet,
  Tag,
  NavigableString,
)
from src.shared import Logger
from .parser_base import ParserBase
from src.api.parsing_results.parsing_result_types import ParsingResult
from src.api.search_links.search_link_types import SourceName

logger = Logger().get_instance()

class ParserCian(ParserBase):
  async def parse(
    self,
    markup: str | bytes,
  ) -> list[ParsingResult]:
    soup = self.parser.with_lxml(markup=markup)
    body = soup.find(name="body")

    card_container_regex = re.compile(r"content")
    price_regex = re.compile(r"\d+")

    items: ResultSet[Tag | NavigableString] | None = body.find_all(attrs={"data-name": "CardComponent"})
    logger.info(f"Parsing {SourceName.cian.value}. Count items: {len(items)}")
    if not items:
      message = f"Не нашел контейнер при парсинге источника \"{SourceName.cian.value}\""
      logger.error(message)
      raise ValueError(message)

    result: list[ParsingResult] = []
    for item in items:
      try:
        item_content_container = item.find(attrs={"data-name": "LinkArea"})

        item_link = item_content_container.find(name="a")
        direct_link = item_link.get("href")

        item_price_container = item_content_container.find(attrs={"data-mark": "MainPrice"})
        price_raw = item_price_container.text
        price_matches = re.findall(pattern=price_regex, string=price_raw)
        price = int("".join(price_matches))

        commission_percent = None
        deposit_percent = None

        parsing_result = ParsingResult(
          direct_link=direct_link,
          price=price,
          commission_percent=commission_percent,
          deposit_percent=deposit_percent,
        )
        result.append(parsing_result)

      except Exception:
        logger.exception(f"При парсинге источника \"{SourceName.cian.value}\" что-то пошло не так")

    return result
