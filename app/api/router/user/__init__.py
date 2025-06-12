from fastapi import APIRouter
from app.api.router.user.admin import AdminRouter
from app.api.router.user.manage import ManageRouter
apiRouter = APIRouter()
apiRouter.include_router(AdminRouter)
apiRouter.include_router(ManageRouter)
