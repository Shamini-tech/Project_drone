from fastapi import APIRouter, WebSocket
from .video_buffer import VideoBuffer
import base64
import cv2

router = APIRouter()

@router.websocket("/ws/video")
async def video_socket(websocket: WebSocket):
    await websocket.accept()
    while True:
        frame = VideoBuffer.get_frame()
        if frame is not None:
            _, buffer = cv2.imencode('.jpg', frame)
            frame_b64 = base64.b64encode(buffer).decode('utf-8')
            await websocket.send_text(frame_b64)
