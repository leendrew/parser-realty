from abc import (
  ABC,
  abstractmethod,
)
from src.shared import Parser
from src.api.parsing_results.parsing_result_types import ParsingResult

class ParserBase(ABC):
  def __init__(self) -> None:
    self.parser = Parser()

  @abstractmethod
  async def parse(
    self,
    markup: str | bytes,
  ) -> list[ParsingResult]:
    pass
