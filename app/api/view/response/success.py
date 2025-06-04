from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any

class SuccessResponse(JSONResponse):
    def __init__(self, message:str, data:Any,**kwargs):
        content = jsonable_encoder({
            "message":str(message),
            "data":data,
        })
        super().__init__(content,**kwargs)

class HTTP_200_OK(SuccessResponse):
    def __init__(self, message: str = "Success", data: Any = None, **kwargs):
        super().__init__(message=message, data=data, status_code=200, **kwargs)