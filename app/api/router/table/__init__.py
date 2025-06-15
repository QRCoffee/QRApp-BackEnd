from fastapi import APIRouter
from beanie import PydanticObjectId
apiRouter = APIRouter(
    prefix="/tables"
)

@apiRouter.get(
    path = "",
)
def get_tables():
    return True

@apiRouter.get(
    path = "{id}",
)
def get_tables(id:PydanticObjectId):
    return True
