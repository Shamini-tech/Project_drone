# backend/video/video_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.video.stream_processor import video_buffer

router = APIRouter()

class FramePayload(BaseModel):
    frame_b64: str

@router.post("/video/frame")
async def post_frame(payload: FramePayload):
    if not payload.frame_b64:
        raise HTTPException(status_code=400, detail="Missing frame")
    await video_buffer.push(payload.frame_b64)
    return {"status":"ok"}
