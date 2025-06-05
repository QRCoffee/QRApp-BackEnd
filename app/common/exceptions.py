from fastapi import status,HTTPException
from typing import Any
class APIException(HTTPException):
    def __init__(self, status_code, message:str = "Refresh or try again later",error:Any | None = None, headers = None):
        detail = {
            "error":error,
            "message":message,
        }
        super().__init__(status_code, detail, headers)

class UnauthorizedException(APIException):
    def __init__(self, message = None, error = "Unauthorized", headers=None):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message, error, headers)

class ForbiddenException(APIException):
    def __init__(self, message = None, error = "Forbidden", headers=None):
        super().__init__(status.HTTP_403_FORBIDDEN, message, error, headers)

class NotFoundException(APIException):
    def __init__(self, message = None, error = "Not Found", headers=None):
        super().__init__(status.HTTP_404_NOT_FOUND, message, error, headers)

class ConflictException(APIException):
    def __init__(self, message = None, error = "Conflict", headers=None):
        super().__init__(status.HTTP_409_CONFLICT, message, error, headers)
