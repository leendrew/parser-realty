from enum import (
  Enum,
  IntEnum,
)

class SearchType(IntEnum):
  rent = 1
  purchase = 2

search_type_title_map = {
  SearchType.rent: "Аренда",
  SearchType.purchase: "Покупка",
}

class SourceName(Enum):
  avito = "avito"
  cian = "cian"
  yandex = "yandex"

source_name_title_map = {
  SourceName.avito: "Авито",
  SourceName.cian: "Циан",
  SourceName.yandex: "Яндекс Недвижимость",
}
