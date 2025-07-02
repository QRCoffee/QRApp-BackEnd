from typing import Dict, List, Optional

from beanie import PydanticObjectId
from fastapi import WebSocket

from app.core.security import ACCESS_JWT
from app.service import userService


class ConnectionManager:
    def __init__(self):
        self.connections: Dict[PydanticObjectId,WebSocket] = {}
        self.groups: Dict[str|PydanticObjectId, Dict] = {}

    async def connect(self, websocket: WebSocket) -> bool:
        token = websocket.query_params.get("token")
        try:
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
            for permission in payload.get("user_permissions",[]):
                self.groups[group][branch].setdefault(permission, [])
                self.groups[group][branch][permission].append(websocket)
            return True
        except Exception:
            await websocket.close(code=1008)
            return False

    async def disconnect(self, websocket: WebSocket):
        # Tìm user_id tương ứng với websocket
        user_id_to_remove = None
        for user_id, ws in self.connections.items():
            if ws == websocket:
                user_id_to_remove = user_id
                break
        if not user_id_to_remove:
            return  # Không tìm thấy user liên kết
        # Xoá khỏi connections
        del self.connections[user_id_to_remove]
        # Lấy user để biết group/branch
        user = await userService.find(user_id_to_remove)
        group = str(user.business.to_ref().id) if user.business else "System"
        branch = str(user.branch.to_ref().id) if user.branch else "None"
        try:
            permission_map = self.groups[group][branch]
            # Duyệt tất cả các permission và xoá websocket
            permissions_to_delete = []
            for permission, sockets in permission_map.items():
                if websocket in sockets:
                    sockets.remove(websocket)
                if not sockets:
                    permissions_to_delete.append(permission)
            # Xoá các permission rỗng
            for permission in permissions_to_delete:
                del permission_map[permission]
            # Nếu không còn permission nào → xoá branch
            if not self.groups[group][branch]:
                del self.groups[group][branch]
            # Nếu không còn branch nào → xoá group
            if not self.groups[group]:
                del self.groups[group]
        except KeyError:
            pass

    async def broadcast(
        self,
        message: str,
        user_ids: Optional[List[PydanticObjectId]] = None,
        business: Optional[str] = None,
        branch: Optional[str] = None,
        permission: Optional[str] = None,
    ):
        sent: set[WebSocket] = set()  # Đảm bảo không gửi trùng WebSocket

        # 1. Gửi theo user_ids nếu có
        if user_ids:
            for uid in user_ids:
                ws = self.connections.get(uid)
                if ws and ws not in sent:
                    await ws.send_text(message)
                    sent.add(ws)

        # 2. Gửi theo group (doanh nghiệp)
        if business:
            group_data = self.groups.get(business)
            if group_data:
                if branch:
                    branch_data = group_data.get(branch)
                    if branch_data:
                        if permission:
                            for ws in branch_data.get(permission, []):
                                if ws not in sent:
                                    await ws.send_text(message)
                                    sent.add(ws)
                        else:
                            for perm_ws_list in branch_data.values():
                                for ws in perm_ws_list:
                                    if ws not in sent:
                                        await ws.send_text(message)
                                        sent.add(ws)
                else:
                    for branch_data in group_data.values():
                        if permission:
                            for ws in branch_data.get(permission, []):
                                if ws not in sent:
                                    await ws.send_text(message)
                                    sent.add(ws)
                        else:
                            for perm_ws_list in branch_data.values():
                                for ws in perm_ws_list:
                                    if ws not in sent:
                                        await ws.send_text(message)
                                        sent.add(ws)

        # 3. Nếu không có user_ids và business => gửi cho tất cả
        if not user_ids and not business:
            for ws in self.connections.values():
                if ws not in sent:
                    await ws.send_text(message)
                    sent.add(ws)

    
manager = ConnectionManager()