# backend/video/video_buffer.py
"""
Simple asyncio Queue buffer for frames. Frame is base64 string.
"""
import asyncio

class VideoBuffer:
    def __init__(self, maxsize=64):
        self.q = asyncio.Queue(maxsize=maxsize)

    async def push(self, frame_b64):
        try:
            await self.q.put(frame_b64)
        except asyncio.QueueFull:
            _ = await self.q.get()
            await self.q.put(frame_b64)

    async def get(self):
        return await self.q.get()

    def empty(self):
        return self.q.empty()
