from enum import Enum

class SourceName(Enum):
  avito = "avito"
  yandex = "yandex"
  cian = "cian"

source_name_title_map = {
  SourceName.avito: "Авито",
  SourceName.yandex: "Яндекс Недвижимость",
  SourceName.cian: "Циан",
}
