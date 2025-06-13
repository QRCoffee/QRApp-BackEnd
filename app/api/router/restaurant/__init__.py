from fastapi import APIRouter

from app.api.router.restaurant.admin import AdminRouter

apiRouter = APIRouter()
apiRouter.include_router(AdminRouter)