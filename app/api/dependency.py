from typing import Optional, List, Literal, Callable
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from app.common.exceptions import HTTP_401_UNAUTHORZIED, HTTP_403_FORBIDDEN
from app.core.security import ACCESS_JWT
from app.common.enum import UserRole,APIError,APIMessage
from app.db import Redis

security = HTTPBearer(auto_error=False)

def permissions(roles: Optional[List[UserRole]] = None) -> Callable:
    """
    Dependency gộp giữa xác thực đăng nhập (JWT Bearer) và kiểm tra quyền truy cập theo vai trò.

    Args:
        roles (Optional[List[UserRole]]): Danh sách các vai trò được phép truy cập. Nếu không truyền, chỉ kiểm tra đăng nhập.

    Returns:
        Callable: Hàm dependency dùng với Depends(), trả về:
                  - payload (dict) nếu chỉ kiểm tra đăng nhập,
                  - True nếu có kiểm tra quyền và hợp lệ.
    """
    def _permissions(
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    ) -> dict:
        if credentials is None or credentials.scheme.lower() != "bearer":
            raise HTTP_401_UNAUTHORZIED(
                error=APIError.INVALID_TOKEN,
                message=APIMessage.INVALID_TOKEN,
            )
        try:
            payload: dict = ACCESS_JWT.decode(credentials.credentials)
            if not Redis.get(payload.get("_id")):
                raise HTTP_401_UNAUTHORZIED(
                    error=APIError.SESSION_EXPIRED,
                    message=APIMessage.SESSION_EXPIRED,
                )
        except Exception:
            raise HTTP_401_UNAUTHORZIED(
                error=APIError.INVALID_TOKEN,
                message=APIMessage.INVALID_TOKEN,
            )
        # Nếu có yêu cầu kiểm tra vai trò
        if roles and payload.get("role") not in [r.value for r in roles]:
            raise HTTP_403_FORBIDDEN(
                error=APIError.PERMISSION_DENIED,
                message=APIMessage.PERMISSION_DENIED,
            )
        payload.pop("password")
        payload.pop("exp")
        return payload
    return _permissions