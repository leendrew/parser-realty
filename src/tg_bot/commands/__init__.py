from .command_start import router as router_start
from .command_show_menu import router as router_show_menu
from .command_menu import router as router_menu
from .command_stop import router as router_stop
from .ui_commands import ui_commands

commands_routers = [
  router_start,
  router_show_menu,
  router_menu,
  router_stop,
]