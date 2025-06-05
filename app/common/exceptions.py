from fastapi import status,HTTPException
class APIException(HTTPException):
    def __init__(self, status_code, detail = None, headers = None):
        super().__init__(status_code, detail, headers)

class NotFoundException(APIException):
    def __init__(self, content=None, headers=None):
        super().__init__(status.HTTP_404_NOT_FOUND, content, headers)
