# backend/video/stream_processor.py
import asyncio
from backend.video.video_buffer import VideoBuffer
from backend.video.video_broadcast import Broadcaster
from backend.ai.inference import infer_from_b64

video_buffer = VideoBuffer()
broadcaster = Broadcaster()

async def video_consumer_loop():
    """
    Background task: gets frames from buffer, runs inference, broadcasts frame and alerts.
    """
    while True:
        frame_b64 = await video_buffer.get()
        try:
            detections, alert, img = infer_from_b64(frame_b64)
        except Exception as e:
            print("Inference error:", e)
            alert = {"type":"NO_THREAT", "detections": [], "timestamp": None}
        # broadcast raw frame to video clients
        await broadcaster.broadcast_video(frame_b64)
        # broadcast alert
        await broadcaster.broadcast_alert(alert)
