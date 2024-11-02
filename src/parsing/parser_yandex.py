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

class ParserYandex(ParserBase):
  async def parse(
    self,
    markup: str | bytes,
  ) -> list[ParsingResult]:
    soup = self.parser.with_lxml(markup=markup)
    body = soup.find(name="body")

    price_regex = re.compile(r"\d+")
    tags_regex = re.compile(r"tagscontainer", re.IGNORECASE)
    commission_regex = re.compile(r"комиссия\s+(\d+)?", re.IGNORECASE)
    deposit_regex = re.compile(r"(залог)", re.IGNORECASE)

    container = body.find(class_="OffersSerp__list")
    if not container:
      message = f"Не нашел контейнер при парсинге источника \"{SourceName.yandex.value}\""
      logger.error(message)
      raise ValueError(message)

    result: list[ParsingResult] = []

    items: ResultSet[Tag | NavigableString] | None = container.find_all(class_="OffersSerpItem__main")
    logger.info(f"Parsing {SourceName.yandex.value}. Count items: {len(items)}")
    for item in items:
      try:
        item_link = item.find(name="a")
        direct_link = "https://realty.ya.ru" + item_link.get("href")

        item_price = item.find(class_="Price")
        price_raw = item_price.text
        price_matches = re.findall(pattern=price_regex, string=price_raw)
        price = int("".join(price_matches))

        commission_percent = 0
        deposit_percent = 0
        item_tags_container = item.find(class_=tags_regex)
        if item_tags_container:
          tags_raw = item_tags_container.text.strip()

          commission_match = re.search(pattern=commission_regex, string=tags_raw)
          if commission_match:
            commission = commission_match.group(1)
            commission_percent = int(commission)

          deposit_match = re.search(pattern=deposit_regex, string=tags_raw)
          if deposit_match:
            deposit_percent = 100

        parsing_result = ParsingResult(
          direct_link=direct_link,
          price=price,
          commission_percent=commission_percent,
          deposit_percent=deposit_percent,
        )
        result.append(parsing_result)

      except Exception:
        logger.exception(f"При парсинге источника \"{SourceName.yandex.value}\" что-то пошло не так")

    return result
