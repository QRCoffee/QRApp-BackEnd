from fastapi import APIRouter, Depends

from app.api.dependency import login_required
from app.api.router.restaurant.admin import AdminRouter
from app.api.router.restaurant.manage import ManageRouter

apiRouter = APIRouter(
    dependencies=[
        Depends(login_required),
    ]
)
apiRouter.include_router(AdminRouter)
apiRouter.include_router(ManageRouter)