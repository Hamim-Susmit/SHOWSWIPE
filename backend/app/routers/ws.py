from collections import defaultdict

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.connections = defaultdict(list)

    async def connect(self, circle_id: str, websocket: WebSocket):
        await websocket.accept()
        self.connections[circle_id].append(websocket)

    def disconnect(self, circle_id: str, websocket: WebSocket):
        if websocket in self.connections.get(circle_id, []):
            self.connections[circle_id].remove(websocket)

    async def broadcast(self, circle_id: str, payload: dict):
        for connection in list(self.connections.get(circle_id, [])):
            await connection.send_json(payload)


manager = ConnectionManager()


@router.websocket("/circle/{circle_id}")
async def circle_ws(websocket: WebSocket, circle_id: str):
    await manager.connect(circle_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(circle_id, websocket)
