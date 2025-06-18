from typing import List, Optional

from beanie import PydanticObjectId
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.common.enum import APIError, APIMessage
from app.common.exceptions import (HTTP_401_UNAUTHORZIED, HTTP_403_FORBIDDEN,
                                   HTTP_404_NOT_FOUND)
from app.core.security import ACCESS_JWT
from app.db import Redis

security = HTTPBearer(auto_error=False)

def login_required(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> bool:
    if credentials is None:
        raise HTTP_401_UNAUTHORZIED(
            error=APIError.UNAUTHORIZED,
            message=APIMessage.UNAUTHORIZED,
        )
    if credentials.scheme.lower() != "bearer":
        raise HTTP_401_UNAUTHORZIED(
            error=APIError.INVALID_TOKEN,
            message=APIMessage.INVALID_TOKEN,
        )
    try:
        payload: dict = ACCESS_JWT.decode(credentials.credentials)
        if not Redis.get(payload.get("user_id")):
            raise HTTP_401_UNAUTHORZIED(
                error=APIError.SESSION_EXPIRED,
                message=APIMessage.SESSION_EXPIRED,
            )
        for key, value in payload.items():
            if key == 'exp':
                continue
            setattr(request.state, key, value)
        return True
    except Exception:
        raise HTTP_401_UNAUTHORZIED(
            error=APIError.INVALID_TOKEN,
            message=APIMessage.INVALID_TOKEN,
        )

def required_role(
    role: List[str] = None
):
    def role_checker(request: Request):
        user_role = request.state.user_role
        if role is not None and user_role not in role:
            raise HTTP_403_FORBIDDEN("Bạn không đủ quyền thực hiện hành động này")
        return True
    return role_checker

def required_permissions(
    permissions: List[int] = None
) -> bool:
    def permission_checker(request: Request):
        user_permissions: List[int] = request.state.user_permissions
        if permissions is not None:
            if not all(perm in user_permissions for perm in permissions):
                raise HTTP_403_FORBIDDEN("Bạn không đủ quyền thực hiện hành động này")
        return True
    return permission_checker

__all__ = ["login_required","required_role","required_permissions","require_restaurant"]