from fastapi.responses import JSONResponse
from typing import Any
from fastapi import status
from fastapi.encoders import jsonable_encoder
class APIResponse(JSONResponse):
    def __init__(self, message:str,data:Any, status_code: int = status.HTTP_200_OK,**kwars):
        content = jsonable_encoder({
            "message":message,
            "data":data,
        })
        super().__init__(content, status_code,**kwars)

class SuccessResponse(APIResponse):
    def __init__(self, message = "Success", data = None, **kwars):
        super().__init__(message, data, status.HTTP_200_OK, **kwars)

class CreatedResponse(APIResponse):
    def __init__(self, message = "Created", data = None, **kwars):
        super().__init__(message, data, status.HTTP_201_CREATED, **kwars)

class NoContentResponse(APIResponse):
    def __init__(self, message = "No Content", data = None, **kwars):
        super().__init__(message, data, status.HTTP_204_NO_CONTENT, **kwars)

class AcceptedResponse(APIResponse):
    def __init__(self, message = "Accepted", data = None, **kwars):
        super().__init__(message, data, status.HTTP_202_ACCEPTED, **kwars)