from beanie import PydanticObjectId
from fastapi import APIRouter

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
def get_table(id:PydanticObjectId):
    return id
