from bs4 import BeautifulSoup

class Parser:
  def __init__(self) -> None:
    self.__instance = BeautifulSoup

  def with_lxml(self, *args, **kwargs) -> BeautifulSoup:
    kwargs["features"] = "lxml"

    return self.__instance(*args, **kwargs)
