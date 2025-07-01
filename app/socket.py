import logging
from typing import Dict, List

from fastapi import WebSocket

from app.core.security import ACCESS_JWT


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.groups: Dict[str, List[WebSocket]] = {}

    def verify_group(cls,client:WebSocket):
        Authorization = client.headers.get("authorization")
        try:
            token = Authorization.split("Bearer ")[1]
            payload: dict = ACCESS_JWT.decode(token)
            logging.getLogger("uvicorn.error").info(
                f"Authenticated WebSocket: user_id={payload.get('user_id')}, role={payload.get('user_role', 'Guest')}"
            )
            return payload.get("user_role","Guest")
        except Exception:
            return "Guest"
    
    async def connect(self, websocket: WebSocket):
        group = self.verify_group(websocket)
        await websocket.accept()
        self.connections.append(websocket)
        if group not in self.groups:
            self.groups[group] = []
        self.groups[group].append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def send_text(self, message: str):
        for connection in self.connections:
            await connection.send_text(message)
    
    async def send_json(self, json: dict):
        for connection in self.connections:
            await connection.send_json(json)

manager = ConnectionManager()