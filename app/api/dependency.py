from typing import Any, Optional

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.common.exceptions import UnauthorizedException
from app.core.security import ACCESS_JWT

security = HTTPBearer(auto_error=False)

def login_required(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Any:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedException("Invalid or missing token")
    try:
        return ACCESS_JWT.decode(credentials.credentials)
    except Exception as e:
        raise UnauthorizedException(
            message="Invalid token",
            error=e.__class__.__name__,
        )