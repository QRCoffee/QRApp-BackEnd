from typing import Any, Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.common.exceptions import UnauthorizedException
from app.core.security import ACCESS_JWT
from app.db import Redis
security = HTTPBearer(auto_error=False)

def login_required(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Any:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedException("Invalid or missing token")
    try:
        payload = ACCESS_JWT.decode(credentials.credentials)
        if not Redis.get(payload.get("_id")):
            raise UnauthorizedException(
                error="SessionInvalid",
                message="phiên đăng nhập hết hạn",
            )
        return payload
    except Exception as e:
        raise UnauthorizedException(
            error=e.__class__.__name__,
            message="phiên đăng nhập hết hạn",
        )