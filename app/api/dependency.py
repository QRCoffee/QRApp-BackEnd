from typing import Optional
from fastapi import Depends
from app.common.exceptions import UnauthorizedException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer(auto_error=False)

def login_required(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedException("Invalid or missing token")
    return credentials.credentials