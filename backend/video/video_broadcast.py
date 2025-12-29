import asyncio
import json
from typing import Set
from fastapi import WebSocket

class Broadcaster:
    def __init__(self):
        self.video_clients: Set[WebSocket] = set()
        self.alert_clients: Set[WebSocket] = set()
        self.telemetry_clients: Set[WebSocket] = set()
        self._lock = asyncio.Lock()

    async def connect(self, ws: WebSocket, kind: str):
        await ws.accept()
        if kind == "video":
            self.video_clients.add(ws)
        elif kind == "alerts":
            self.alert_clients.add(ws)
        elif kind == "telemetry":
            self.telemetry_clients.add(ws)

    async def disconnect(self, ws: WebSocket):
        if ws in self.video_clients: self.video_clients.remove(ws)
        if ws in self.alert_clients: self.alert_clients.remove(ws)
        if ws in self.telemetry_clients: self.telemetry_clients.remove(ws)

    async def broadcast_video(self, frame_b64):
        to_remove = []
        for ws in set(self.video_clients):
            try:
                await ws.send_text(frame_b64)
            except Exception:
                to_remove.append(ws)
        for ws in to_remove:
            await self.disconnect(ws)

    async def broadcast_alert(self, alert_obj):
        payload = json.dumps(alert_obj)
        to_remove = []
        for ws in set(self.alert_clients):
            try:
                await ws.send_text(payload)
            except Exception:
                to_remove.append(ws)
        for ws in to_remove:
            await self.disconnect(ws)

    async def broadcast_telemetry(self, telemetry):
        payload = json.dumps(telemetry)
        to_remove = []
        for ws in set(self.telemetry_clients):
            try:
                await ws.send_text(payload)
            except Exception:
                to_remove.append(ws)
        for ws in to_remove:
            await self.disconnect(ws)

# ← Add this line at the bottom
broadcaster = Broadcaster()
