from fastapi.responses import JSONResponse
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from typing import Any

class ErrorResponse(JSONResponse):
    def __init__(self, message:str, error:Any,**kwargs):
        content = jsonable_encoder({
            "message":str(message),
            "error":error,
        })
        super().__init__(content,**kwargs)

class CustomHTTPException(HTTPException):
    def __init__(self, status_code, detail = None, headers = None):
        super().__init__(status_code, detail, headers)

class HTTP_400_BAD_REQUEST(ErrorResponse):
    def __init__(self, message: str = "Bad Request", error: Any = None, **kwargs):
        super().__init__(message=message, error=error, status_code=400, **kwargs)

class HTTP_401_UNAUTHORIZED(ErrorResponse):
    def __init__(self, message: str = "Unauthorized", error: Any = None, **kwargs):
        super().__init__(message=message, error=error, status_code=401, **kwargs)

class HTTP_403_FORBIDDEN(ErrorResponse):
    def __init__(self, message: str = "Forbidden", error: Any = None, **kwargs):
        super().__init__(message=message, error=error, status_code=403, **kwargs)

class HTTP_404_NOT_FOUND(ErrorResponse):
    def __init__(self, message: str = "Not Found", error: Any = None, **kwargs):
        super().__init__(message=message, error=error, status_code=404, **kwargs)

class HTTP_409_CONFLICT(ErrorResponse):
    def __init__(self, message: str = "Conflict", error: Any = None, **kwargs):
        super().__init__(message=message, error=error, status_code=409, **kwargs)

class HTTP_422_VALIDATION_ERROR(ErrorResponse):
    def __init__(self, message: str = "Validation Error", error: Any = None, **kwargs):
        super().__init__(message=message, error=error, status_code=422, **kwargs)

class HTTP_500_INTERNAL_SERVER_ERROR(ErrorResponse):
    def __init__(self, message: str = "Interal Server Error", error: Any = None, **kwargs):
        super().__init__(message=message, error=error, status_code=500, **kwargs)