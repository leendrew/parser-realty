from enum import Enum

class KeyboardMenuKey(Enum):
  home = "home"
  back = "back"
  my_links = "my_links"
  add_link = "add_link"

class KeyboardAddLinkKey(Enum):
  home = "home"
  reset = "reset"

class KeyboardMyLinkKey(Enum):
  home = "home"
  edit_link = "edit_link"
  edit_name = "edit_name"
  toggle_active = "toggle_active"
  delete_link = "delete_link"

class KeyboardStopKey(Enum):
  home = "home"
  confirm = "confirm"
  reject = "reject"
