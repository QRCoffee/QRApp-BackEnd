from fastapi import APIRouter, Depends, File, Request, UploadFile

from app.api.dependency import required_role
from app.common.enum import UserRole
from app.common.exceptions import HTTP_400_BAD_REQUEST
from app.common.responses import APIResponse
from app.db import QRCode
from app.schema.user import ProfileUpdate, UserDetailResponse, UserResponse
from app.service import userService

ManageRouter = APIRouter(
    tags = ["User: Self"],
)

@ManageRouter.post(
    path = "/upload-avatar",
    name = "Upload Avatar",
    status_code=201,
    response_model = APIResponse[UserResponse]
)
async def upload_avatar(request:Request,file: UploadFile = File(description="Ảnh đại diện")):
    from io import BytesIO

    from PIL import Image
    if file.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTP_400_BAD_REQUEST("Chỉ chấp nhận định dạng ảnh: jpg, jpeg, png, webp")
    file_bytes = await file.read()
    if len(file_bytes) > 2 * 1024 * 1024:
        raise HTTP_400_BAD_REQUEST(f"Kích thước ảnh tối đa: 2MB")
    try:
        image = Image.open(BytesIO(file_bytes))
        image.verify()  
        image = Image.open(BytesIO(file_bytes))
        image = image.convert("RGB")
    except Exception:
        raise HTTP_400_BAD_REQUEST("Ảnh không hợp lệ")
    buffer = BytesIO()
    image.save(
        fp=buffer, 
        format="WEBP", 
        quality=85
    )
    buffer.seek(0)
    webp_bytes = buffer.read()
    user_id = str(request.state.user_id)
    object_name = QRCode.upload(
        object=webp_bytes,
        object_name=user_id,
        content_type="image/webp"
    )
    user = await userService.update(
        id = user_id,
        data = ProfileUpdate(
            image_url = QRCode.get_url(object_name),
        )
    )
    return APIResponse(data=user)


@ManageRouter.get(
    path = "/me",
    name  = "Self",
    status_code=200,
    response_model=APIResponse[UserDetailResponse],
)
async def profile(request: Request):
    user = await userService.find_one_by(value=request.state.user_id)
    return APIResponse(
        data=user
    )

@ManageRouter.put(
    path = "/me",
    name = "Update Profile",
    status_code=200,
    response_model=APIResponse[UserDetailResponse],
    dependencies = [
        Depends(required_role([
            UserRole.MANAGER,
            UserRole.ADMIN
        ]))
    ]
)
async def update(data:ProfileUpdate,request:Request):
    await userService.update(
        id = request.state.user_id,
        data = data.model_dump(exclude_none=True)
    )
    user = await userService.find_one_by(value=request.state.user_id)
    return APIResponse(
        data=user
    )