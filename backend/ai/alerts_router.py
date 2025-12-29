from fastapi import APIRouter, WebSocket
from backend.utils.alerts import push_alert  # this file EXISTS in utils

router = APIRouter()

@router.websocket("/ws/alerts")
async def alerts_ws(websocket: WebSocket):
    await websocket.accept()
    push_alert("Alert WS connected")

    try:
        while True:
            msg = await websocket.receive_text()
            push_alert(f"Received alert: {msg}")
    except Exception:
        pass
