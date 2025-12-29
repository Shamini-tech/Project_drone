# backend/ai/telemetry_ws.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json

router = APIRouter(
    prefix="/ai",
    tags=["ai-telemetry"]
)

@router.websocket("/ws/telemetry")
async def ai_telemetry_ws(websocket: WebSocket):
    """
    WebSocket for receiving AI-specific telemetry data.
    This does NOT interfere with backend/telemetry/telemetry_ws.py
    """
    await websocket.accept()

    try:
        while True:
            # Receive raw text from client
            raw = await websocket.receive_text()

            # Try to decode JSON
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_json({"error": "Invalid JSON"})
                continue

            # Extract only AI-specific telemetry fields
            ai_packet = {
                "object_count": data.get("object_count"),
                "detected_classes": data.get("detected_classes"),
                "confidence_scores": data.get("confidence_scores"),
                "processing_time_ms": data.get("processing_time_ms"),
                "frame_id": data.get("frame_id"),
            }

            # Echo back or forward to your AI processor (extend later)
            await websocket.send_json({
                "status": "received",
                "ai_telemetry": ai_packet
            })

    except WebSocketDisconnect:
        print("AI telemetry WebSocket disconnected")
