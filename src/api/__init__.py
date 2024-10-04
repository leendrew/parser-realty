from fastapi import APIRouter
# from .search_links.search_link_controller import router as search_link_router
# from .parsing_results.parsing_result_controller import router as parsing_result_router

api_router = APIRouter(
  prefix="/api",
)

routers = [
  # search_link_router,
  # parsing_result_router,
]

for router in routers:
  api_router.include_router(router)
