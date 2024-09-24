import re
from bs4 import (
  ResultSet,
  Tag,
  NavigableString,
)
from src.shared import Logger
from .parser_base import ParserBase
from src.api.parsing_results.parsing_result_types import (
  ParsingResult,
  HousingType,
)
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
    title_flat_regex = re.compile(r"([^,]+),\s*(\d+(?:[.,]\d+)?).*,\s*([0-9/]+)")
    title_house_regex = re.compile(r"()(\d+).+м²()")
    housing_type_regex = re.compile(r"(квартира)?(комната)?", re.MULTILINE)
    flat_room_type_regex = re.compile(r"(\d+)")
    deposit_regex = re.compile(r"\d+")
    commission_percent_regex = re.compile(r"(\d+)")
    item_metro_station_root_container_regex = re.compile(r"geo-root")
    item_metro_station_icon_regex = re.compile(r"geo-icons")
    # ¯\_(ツ)_/¯ source specific
    metro_station_name_by_geo_map = {
      "мурино": "Девяткино",
    }

    container = body.find(attrs={"data-marker": "catalog-serp"})
    if not container:
      message = f"Не нашел контейнер при парсинге источника \"{SourceName.avito}\""
      logger.error(message)
      raise Exception(message)

    result: list[ParsingResult] = []

    items: ResultSet[Tag | NavigableString] | None = container.find_all(attrs={"data-marker": "item"})
    for item in items:
      try:
        item_body = item.find(class_=item_body_regex)

        item_link = item_body.find(attrs={"itemprop": "url"})
        direct_link = "https://www.avito.ru" + item_link.get("href")

        item_title = item_link.find(attrs={"itemprop": "name"})
        title_content = item_title.text.lower()

        title_match = re.search(pattern=title_flat_regex, string=title_content)
        if not title_match:
          title_match = re.search(pattern=title_house_regex, string=title_content)
        type, flat_area, floor = title_match.groups()
        if not floor:
          floor = "1"

        housing_type = HousingType.house
        housing_type_match = re.search(pattern=housing_type_regex, string=type)
        if housing_type_match:
          flat = housing_type_match.group(1)
          room = housing_type_match.group(2)
          if flat:
            housing_type = HousingType.flat
          if room:
            housing_type = HousingType.room

        flat_room_type_match = re.search(pattern=flat_room_type_regex, string=type)
        flat_room_type = flat_room_type_match and flat_room_type_match.group(1)
        flat_room_type = flat_room_type and int(flat_room_type) or 0
        if housing_type is HousingType.house:
          flat_room_type = -1

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

        metro_station_name = None
        item_metro_station_root_container = item_body.find(class_=item_metro_station_root_container_regex)
        if item_metro_station_root_container:
          item_metro_station_name = item_metro_station_root_container.text.strip().lower()

          if item_metro_station_name in metro_station_name_by_geo_map.keys():
            metro_station_name = metro_station_name_by_geo_map[item_metro_station_name]
          else:
            item_metro_station_name = item_metro_station_root_container.find(class_=item_metro_station_icon_regex)
            if item_metro_station_name:
              metro_station_name = item_metro_station_name.next_sibling.text.strip()

        parsing_result = ParsingResult(
          direct_link=direct_link,
          housing_type=housing_type,
          flat_room_type=flat_room_type,
          floor=floor,
          flat_area=flat_area,
          price=price,
          commission_percent=commission_percent,
          deposit_percent=deposit_percent,
          metro_station_name=metro_station_name,
        )
        result.append(parsing_result)

      except Exception:
        logger.exception(f"При парсинге источника \"{SourceName.avito}\" что-то пошло не так")

    return result
