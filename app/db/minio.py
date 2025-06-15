import io
import json
from minio import Minio
from typing import Any

class MinIO:
    def __init__(self,
        bucket_name: str,
        endpoint:str = "localhost:9000",
        access_key: str | None = None,
        secret_key: str | None = None,
        secure: bool = False,
        public: bool = False,
    ):
        self.endpoint = endpoint
        self.secure = secure
        self.bucket_name = bucket_name
        self.client = Minio(
            endpoint=self.endpoint,
            access_key= access_key,
            secret_key= secret_key,
            secure = self.secure,
        )
        self.initialize(public)

    def initialize(self,public: bool = False):
        if not self.client.bucket_exists(self.bucket_name):
            self.client.make_bucket(self.bucket_name)
            if public:
                policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"AWS": "*"},
                            "Action": ["s3:GetObject"],
                            "Resource": [f"arn:aws:s3:::{self.bucket_name}/*"]
                        }
                    ]
                }
                self.client.set_bucket_policy(
                    bucket_name = self.bucket_name,
                    policy = json.dumps(policy)
                )

    def upload(self, object: Any, object_name: str = None, content_type: str = "application/octet-stream") -> str:
        if object_name is None:
            object_name = f"{uuid.uuid4().hex}"

        if isinstance(object, bytes):
            data = io.BytesIO(object)
            size = len(object)
        elif hasattr(object, 'read'):
            data = object
            data.seek(0, io.SEEK_END)
            size = data.tell()
            data.seek(0)
        else:
            raise ValueError("Unsupported object type. Provide bytes or file-like object.")

        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_name,
            data=data,
            length=size,
            content_type=content_type
        )
        url = f"{"https" if self.secure else "http"}://{self.endpoint}/{self.bucket_name}/{object_name}"
        return url
    
QRCode = MinIO(
    bucket_name = "QRCode",
    access_key = "admin",
    secret_key="admin123456",
    public=True,
)

__all__ = ["QRCode"]