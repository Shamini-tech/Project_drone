from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.video.video_broadcast import broadcaster

router = APIRouter()

@router.websocket("/ws/alerts")
async def ws_alerts(ws: WebSocket):
    await ws.accept()                # Important!
    await broadcaster.connect(ws, "alerts")
    try:
        while True:
            msg = await ws.receive_text()  # keep connection alive
    except WebSocketDisconnect:
        await broadcaster.disconnect(ws)
    except Exception:
        await broadcaster.disconnect(ws)
