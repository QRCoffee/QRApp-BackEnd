import uuid

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class TraceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 🔍 Lấy request_id từ cookie nếu có, ngược lại tạo mới
        request_id = request.cookies.get("request_id") or str(uuid.uuid4())
        # 🧠 Gắn vào request.state nếu cần truy vết trong view
        request.state.request_id = request_id
        # 📤 Gửi response sau khi xử lý
        response: Response = await call_next(request)
        # 🔁 Luôn gắn lại trace-id để gia hạn 15 phút tính từ mỗi request
        response.set_cookie(
            key="request_id",
            value=request_id,
            max_age=900,  # 15 phút = 900s
            httponly=True,  # Ẩn với JavaScript
            samesite="Lax",  # Lax giúp cookie vẫn hoạt động trong hầu hết request POST
            path="/",
        )
        return response
