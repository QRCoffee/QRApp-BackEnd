from fastapi import status,HTTPException
from typing import Any
class APIException(HTTPException):
    def __init__(self, status_code, message:str = "Something went wrong. Refresh or try again later",error:Any | None = None, headers = None):
        detail = {
            "message":message,
            "error":error,
        }
        super().__init__(status_code, detail, headers)

class UnauthorizedException(APIException):
    def __init__(self, message = "Unauthorized", error = None, headers=None):
        super().__init__(status.HTTP_401_UNAUTHORIZED, message, error, headers)

class ForbiddenException(APIException):
    def __init__(self, message = "Forbidden", error = None, headers=None):
        super().__init__(status.HTTP_403_FORBIDDEN, message, error, headers)

class NotFoundException(APIException):
    def __init__(self, message = "Not Found", error = None, headers=None):
        super().__init__(status.HTTP_404_NOT_FOUND, message, error, headers)

class ConflictException(APIException):
    def __init__(self, message = "Conflict", error = None, headers=None):
        super().__init__(status.HTTP_409_CONFLICT, message, error, headers)
