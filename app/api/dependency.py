from api.view.response import CustomHTTPException
from fastapi import HTTPException
from fastapi import Header
def login_required(Authorization: str = Header(None)) -> str:
    if Authorization is None or not Authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail={
                "message":"Unauthorized",
                "error":"Invalid or missing Bearer token"
            }
            
        )
    return Authorization.removeprefix("Bearer ").strip()