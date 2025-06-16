from io import BytesIO
from typing import Optional

import httpx
from beanie import Insert, Link, after_event, before_event
from PIL import Image
from pydantic import Field

from app.common.exceptions import HTTP_409_CONFLICT
from app.models import Area

from .base import Base


class Table(Base):
    name: str = Field(...,nullable=False)
    area: Link[Area] = Field(...,nullable=False)
    capacity: int = Field(default=1,nullable=False,ge=0)
    image_url: Optional[str] = Field(default=None)
    qr_url: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)

    @before_event(Insert)
    async def unique_table_in_area(self):
        from app.service import tableService
        tables = await tableService.find_many_by(conditions={
            "area._id":self.area.id
        })
        if any(table.name.lower() == self.name.lower() for table in tables):
            raise HTTP_409_CONFLICT(f"Bàn '{self.name}' đã tồn tại trong khu vực này")
    
    @after_event(Insert)
    async def set_qr_url(self):
        from app.db import QRCode
        table_id = self.id
        url = f"https://quickchart.io/qr?text={table_id}&size=300"
        response = httpx.get(url)
        # Convert PNG to WebP using Pillow
        img = Image.open(BytesIO(response.content))
        webp_buffer = BytesIO()
        img.save(webp_buffer, format="WEBP", quality=80, optimize=True)
        webp_bytes = webp_buffer.getvalue()

        # Generate unique filename
        filename = f"qr-codes/{table_id}.webp"
        QRCode.client.put_object(
            bucket_name=QRCode.bucket_name,
            object_name=filename,
            data=BytesIO(webp_bytes),
            length=len(webp_bytes),
            content_type='image/webp'
        )
        self.qr_url = f"http://localhost:9000/{QRCode.bucket_name}/{filename}"
        await self.save()