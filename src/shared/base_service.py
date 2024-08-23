from abc import ABC
from src.shared import SessionDependency

class BaseService(ABC):
  def __init__(self, session: SessionDependency) -> None:
    self.session = session
