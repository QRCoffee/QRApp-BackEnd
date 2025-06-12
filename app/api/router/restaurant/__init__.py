from fastapi import APIRouter,Depends
from app.schema.restaurant import RestaurantCreate
from app.common.exceptions import HTTP_404_NOT_FOUND
from app.common.responses import APIResponse
from app.models import Restaurant
from app.api.dependency import permissions
from app.common.enum import UserRole
from beanie import PydanticObjectId
from app.service import userService,restaurantService
from app.api.router.restaurant.admin import AdminRouter
from app.api.router.restaurant.manager import ManageRouter
apiRouter = APIRouter(
    prefix="/restaurants",
)

apiRouter.include_router(AdminRouter)
# apiRouter.include_router(ManageRouter)