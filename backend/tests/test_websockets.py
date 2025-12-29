# test_websockets.py
import asyncio
import websockets

async def listen_alerts():
    uri = "ws://localhost:8000/ws/alerts"
    async with websockets.connect(uri) as ws:
        print("Connected to alerts WS")
        msg = await ws.recv()
        print("Alert:", msg)

asyncio.run(listen_alerts())
