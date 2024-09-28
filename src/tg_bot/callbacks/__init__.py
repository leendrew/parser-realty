from .callback_show_menu import router as callback_show_menu_router
from .callback_menu import router as callback_menu_router
from .callback_my_link import router as callback_my_link_router
from .callback_stop import router as callback_stop_router

callbacks_routers = [
  callback_show_menu_router,
  callback_menu_router,
  callback_my_link_router,
  callback_stop_router,
]