from fastapi import Header,Depends
from typing import Optional
from app.common.exceptions import UnauthorizedException
from app.core.security import JWTSecurity

def login_required(
    Authorization: Optional[str] = Header(None),
    _ = Depends(JWTSecurity)  
):
    if Authorization is None or not Authorization.startswith("Bearer "):
        raise UnauthorizedException(
            error = "Invalid or missing token",
        )
    return Authorization.removeprefix("Bearer ")