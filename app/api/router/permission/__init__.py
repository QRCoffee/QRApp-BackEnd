from typing import List, Optional

from fastapi import APIRouter, Depends, Query

from app.api.dependency import login_required, required_role
from app.common.enum import UserRole
from app.common.responses import APIResponse
from app.core.config import settings
from app.schema.permission import PermissionResponse
from app.service import permissionService

PermissionRouter = APIRouter(
    prefix="/permissions",
    tags = ["Admin: Permission"],
    dependencies=[
        Depends(login_required),
        Depends(required_role([UserRole.ADMIN])),
    ]
)

@PermissionRouter.get(
    path = "",
    status_code = 200,
    response_model=APIResponse[List[PermissionResponse]],
)
async def get_permissions(
    page: int = Query(default=1,ge=1),
    limit: int = Query(default=settings.PAGE_SIZE, ge=1, le=50),
    code: Optional[str] = Query(default=""),
    description: Optional[str] = Query(default=None)
):
    conditions = {}
    if description:
        conditions['description'] = {
            "$regex": description,
            "$options": "i"
        }
    permissions = await permissionService.find_many_by(
        conditions,
        skip=(page - 1) * limit,
        limit=limit,
    )
    permissions = [permission for permission in permissions if str(permission.code).find(code) != -1]
    return APIResponse(data=permissions)