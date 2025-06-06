from typing import Optional,Any
from fastapi import Depends
from app.core.security import ACCESS_JWT
from app.common.exceptions import UnauthorizedException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import ExpiredSignatureError, InvalidTokenError


security = HTTPBearer(auto_error=False)

def login_required(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Any:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise UnauthorizedException("Invalid or missing token")
    try:
        return ACCESS_JWT.decode(credentials.credentials)
    except ExpiredSignatureError:
        raise UnauthorizedException("Token has expired. Please log in again.")
    except InvalidTokenError:
        raise UnauthorizedException("Invalid token. Please log in again.")
    