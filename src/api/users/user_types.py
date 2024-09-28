from uuid import UUID
from pydantic import BaseModel

class UserSummary(BaseModel):
  id: UUID
  search_links_count: int
  parsing_results_count: int
