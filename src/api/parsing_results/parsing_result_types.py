from pydantic import BaseModel

class ParsingResult(BaseModel):
  direct_link: str
  price: int
  commission_percent: int | None
  deposit_percent: int | None
