from enum import Enum
from typing import Any

from fastapi import HTTPException, status


class Error(str, Enum):
    SUCCESS = "SUCCESS"
    USERNAME_CONFLICT = "USERNAME_CONFLICT"
    PHONE_CONFLICT = "PHONE_CONFLICT"
    UNAUTHORIZED = "UNAUTHORIZED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INVALID_TOKEN = "INVALID_TOKEN"
    SESSION_EXPIRED = "SESSION_EXPIRED"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    SERVER_ERROR = "SERVER_ERROR"

class HTTP_ERROR(HTTPException):
    def __init__(self, status_code, message:str = "Refresh or try again later",error:Any | None = None, headers = None):
        detail = {
            "error":error,
            "message":message,
        }
        super().__init__(status_code, detail, headers)

class HTTP_400_BAD_REQUEST(HTTP_ERROR):
    def __init__(self, message = None, error = "BAD_REQUEST", headers=None):
        super().__init__(status.HTTP_400_BAD_REQUEST, message, error, headers)
class HTTP_401_UNAUTHORZIED(HTTP_ERROR):
    def __init__(self, message = None, error = "UNAUTHORIZED", headers=None):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message, error, headers)

class HTTP_403_FORBIDDEN(HTTP_ERROR):
    def __init__(self, message = None, error = "FORBIDDEN", headers=None):
        super().__init__(status.HTTP_403_FORBIDDEN, message, error, headers)

class HTTP_404_NOT_FOUND(HTTP_ERROR):
    def __init__(self, message = None, error = "NOT_FOUND", headers=None):
        super().__init__(status.HTTP_404_NOT_FOUND, message, error, headers)

class HTTP_409_CONFLICT(HTTP_ERROR):
    def __init__(self, message = None, error = "CONFLICT", headers=None):
        super().__init__(status.HTTP_409_CONFLICT, message, error, headers)
