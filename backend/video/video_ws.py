# backend/video/video_ws.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.video.video_broadcast import broadcaster

router = APIRouter()

# Video WebSocket
@router.websocket("/ws/video")
async def ws_video(ws: WebSocket):
    await broadcaster.connect(ws, "video")
    try:
        while True:
            msg = await ws.receive_text()  # keep connection alive
    except WebSocketDisconnect:
        await broadcaster.disconnect(ws)
    except Exception:
        await broadcaster.disconnect(ws)

# Alerts WebSocket
@router.websocket("/ws/alerts")
async def ws_alerts(ws: WebSocket):
    await broadcaster.connect(ws, "alerts")
    try:
        while True:
            msg = await ws.receive_text()
    except WebSocketDisconnect:
        await broadcaster.disconnect(ws)
    except Exception:
        await broadcaster.disconnect(ws)

# Telemetry WebSocket
@router.websocket("/ws/telemetry")
async def ws_telemetry(ws: WebSocket):
    await broadcaster.connect(ws, "telemetry")
    try:
        while True:
            msg = await ws.receive_text()
    except WebSocketDisconnect:
        await broadcaster.disconnect(ws)
    except Exception:
        await broadcaster.disconnect(ws)
