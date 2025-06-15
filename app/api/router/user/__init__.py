from fastapi import APIRouter, Depends

from app.api.dependency import login_required
from app.api.router.permission import PermissionRouter
from app.api.router.user.admin import AdminRouter
from app.api.router.user.manage import ManageRouter

apiRouter = APIRouter(
    dependencies=[
        Depends(login_required)
    ]
)
apiRouter.include_router(ManageRouter)
apiRouter.include_router(AdminRouter)
apiRouter.include_router(PermissionRouter)
