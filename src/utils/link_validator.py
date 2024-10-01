import re
from src.api.search_links.search_link_types import SourceName

class LinkValidator:
  @staticmethod
  def is_valid_https(link: str) -> bool:
    return link.startswith("https://")

  @staticmethod
  def get_link_source(link: str) -> SourceName | None:
    https_part_regex = "https:\/\/"
    subdomain_part_regex = ".*\."
    domain_part_regex = "\.[^\/]*"

    regex_link_by_source_map = {
      SourceName.avito: re.compile(pattern=rf"^{https_part_regex}www\.avito{domain_part_regex}"),
      SourceName.yandex: re.compile(rf"^{https_part_regex}realty\.ya{domain_part_regex}"),
      SourceName.cian: re.compile(rf"^{https_part_regex}{subdomain_part_regex}cian{domain_part_regex}"),
    }

    for source, regex in regex_link_by_source_map.items():
      is_match = bool(re.match(
        pattern=regex,
        string=link,
      ))

      if is_match:
        return source

    return None
