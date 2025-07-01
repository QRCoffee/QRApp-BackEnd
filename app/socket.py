from typing import Dict, List, Optional

from beanie import PydanticObjectId
from fastapi import WebSocket

from app.core.security import ACCESS_JWT
from app.service import userService


class ConnectionManager:
    def __init__(self):
        self.connections: Dict[PydanticObjectId,WebSocket] = {}
        self.groups: Dict[str|PydanticObjectId, Dict] = {}

    async def connect(self, websocket: WebSocket):
        Authorization = websocket.headers.get("authorization")
        try:
            token = Authorization.split("Bearer ")[1]
            payload: dict = ACCESS_JWT.decode(token)
            user = await userService.find(payload.get('user_id'))
            group =  str(user.business.to_ref().id) if user.business else "System"
            branch =  str(user.branch.to_ref().id) if user.branch else "None"
            role =  str(user.role)
            # Wait for connection
            await websocket.accept()
            # Add to list connections
            self.connections[user.id] = websocket
            # Add to group
            self.groups.setdefault(group, {})
            self.groups[group].setdefault(branch, {})
            self.groups[group][branch].setdefault(role, [])
            self.groups[group][branch][role].append(websocket)
        except Exception:
            await websocket.close(code=1008)

    async def disconnect(self, websocket: WebSocket):
        # Remove in connections
        user_id_to_remove = None
        for user_id, ws in self.connections.items():
            if ws == websocket:
                user_id_to_remove = user_id
                break
        if not user_id_to_remove:
            return  # Không có user nào liên kết với websocket này
        del self.connections[user_id_to_remove]
        # Remove in groups
        user = await userService.find(user_id_to_remove)
        group = str(user.business.to_ref().id) if user.business else "System"
        branch = str(user.branch.to_ref().id) if user.branch else "None"
        role = str(user.role)
        try:
            sockets = self.groups[group][branch][role]
            if websocket in sockets:
                sockets.remove(websocket)
            # Nếu list socket trống thì xóa role
            if not self.groups[group][branch][role]:
                del self.groups[group][branch][role]
            # Nếu role trống ⇒ xóa branch
            if not self.groups[group][branch]:
                del self.groups[group][branch]
            # Nếu branch trống ⇒ xóa group
            if not self.groups[group]:
                del self.groups[group]
        except KeyError:
            pass

    async def broadcast(
        self,
        message: str,
        user_ids: Optional[List[PydanticObjectId]] = None,
        group: Optional[str] = None,
        branch: Optional[str] = None,
        role: Optional[str] = None,
    ):
        # Nếu chỉ định user cụ thể
        if user_ids:
            for uid in user_ids:
                ws = self.connections.get(uid)
                if ws:
                    await ws.send_text(message)
        # Chỉ định group cụ thể
        if group:
            group_data = self.groups.get(group, {})
            if branch:
                branch_data = group_data.get(branch, {})
                if role:
                    # Gửi cho role cụ thể
                    for ws in branch_data.get(role, []):
                        await ws.send_text(message)
                else:
                    # Gửi cho toàn bộ role trong branch
                    for role_ws in branch_data.values():
                        for ws in role_ws:
                            await ws.send_text(message)
            else:
                # Gửi cho toàn bộ các branch
                for branch_data in group_data.values():
                    for role_ws in branch_data.values():
                        for ws in role_ws:
                            await ws.send_text(message)
            return
        # Gửi tất cả nếu ko truyền gì
        if not user_ids and not group:
            for ws in self.connections.values():
                await ws.send_text(message)
    
manager = ConnectionManager()