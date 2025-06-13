from fastapi import APIRouter

from app.api.router.restaurant.admin import AdminRouter
from app.api.router.restaurant.manage import ManageRouter

apiRouter = APIRouter()
apiRouter.include_router(AdminRouter)
apiRouter.include_router(ManageRouter)