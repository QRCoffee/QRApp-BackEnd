from typing import Any
from app.common.enum import APIError
from fastapi import HTTPException, status


class APIException(HTTPException):
    def __init__(self, status_code, message:str = "Refresh or try again later",error:Any | None = None, headers = None):
        detail = {
            "error":error,
            "message":message,
        }
        super().__init__(status_code, detail, headers)

class HTTP_401_UNAUTHORZIED(APIException):
    def __init__(self, message = None, error = APIError.UNAUTHORIZED, headers=None):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message, error, headers)

class HTTP_403_FORBIDDEN(APIException):
    def __init__(self, message = None, error = APIError.PERMISSION_DENIED, headers=None):
        super().__init__(status.HTTP_403_FORBIDDEN, message, error, headers)

class HTTP_404_NOT_FOUND(APIException):
    def __init__(self, message = None, error = "Not Found", headers=None):
        super().__init__(status.HTTP_404_NOT_FOUND, message, error, headers)

class HTTP_409_CONFLICT(APIException):
    def __init__(self, message = None, error = "Conflict", headers=None):
        super().__init__(status.HTTP_409_CONFLICT, message, error, headers)
