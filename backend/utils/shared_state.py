# backend/utils/shared_state.py
import asyncio
from typing import Dict, Any

class SharedState:
    def __init__(self):
        self._telemetry = {}
        self._latest_frame = None
        self._lock = asyncio.Lock()

    async def set_frame(self, frame_bytes):
        async with self._lock:
            self._latest_frame = frame_bytes

    async def get_frame(self):
        async with self._lock:
            return self._latest_frame

    def update_telemetry(self, telemetry: Dict[str, Any]):
        # Called from threaded MQTT callback -> sync update
        self._telemetry.update(telemetry)

    def get_telemetry(self):
        return self._telemetry.copy()

_shared_state = SharedState()

def get_shared_state():
    return _shared_state
