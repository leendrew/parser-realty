from abc import ABC
from .db_service import SessionDependency

class BaseService(ABC):
  def __init__(self, session: SessionDependency) -> None:
    self.session = session
