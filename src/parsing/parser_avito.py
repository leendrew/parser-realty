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

class ParserAvito(ParserBase):
  async def parse(
    self,
    markup: str | bytes,
  ) -> list[ParsingResult]:
    soup = self.parser.with_lxml(markup=markup)
    body = soup.find(name="body")

    item_body_regex = re.compile(r"item-body")
    deposit_regex = re.compile(r"\d+")
    commission_percent_regex = re.compile(r"(\d+)")

    container = body.find(attrs={"data-marker": "catalog-serp"})
    if not container:
      message = f"Не нашел контейнер при парсинге источника \"{SourceName.avito.value}\""
      logger.error(message)
      raise ValueError(message)

    result: list[ParsingResult] = []

    items: ResultSet[Tag | NavigableString] | None = container.find_all(attrs={"data-marker": "item"})
    for item in items:
      try:
        item_body = item.find(class_=item_body_regex)

        item_link = item_body.find(attrs={"itemprop": "url"})
        direct_link = "https://www.avito.ru" + item_link.get("href")

        item_price = item_body.find(attrs={"itemprop": "price"})
        price = int(item_price.get("content"))

        deposit_percent = None
        commission_percent = None
        item_params = item_body.find(attrs={"data-marker": "item-specific-params"})
        if item_params:
          item_params_text = item_params.text
          arr = item_params_text.split("·")
          deposit_raw = arr[0]
          commission_raw = arr[1]

          deposit_matches = re.findall(pattern=deposit_regex, string=deposit_raw)
          deposit = int("".join(deposit_matches))
          deposit_percent = 0
          if deposit:
            deposit_percent = int(deposit / price * 100)

          commission_match = re.search(pattern=commission_percent_regex, string=commission_raw)
          commission = commission_match and commission_match.group(1)
          commission_percent = commission and int(commission) or 0

        parsing_result = ParsingResult(
          direct_link=direct_link,
          price=price,
          commission_percent=commission_percent,
          deposit_percent=deposit_percent,
        )
        result.append(parsing_result)

      except Exception:
        logger.exception(f"При парсинге источника \"{SourceName.avito.value}\" что-то пошло не так")

    return result
