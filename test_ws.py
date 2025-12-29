# Save this as test_ws.py and run: python test_ws.py
import asyncio
import websockets

endpoints = {
    "video": "ws://localhost:8000/ws/video",
    "alerts": "ws://localhost:8000/ws/alerts",
    "telemetry": "ws://localhost:8000/ws/telemetry"
}

async def test_ws(name, uri):
    try:
        async with websockets.connect(uri) as ws:
            print(f"[{name}] Connected")
            for _ in range(3):  # receive 3 messages for testing
                msg = await ws.recv()
                if name == "video":
                    print(f"[{name}] Frame base64 preview: {msg[:100]}...")
                else:
                    print(f"[{name}] Message: {msg}")
    except Exception as e:
        print(f"[{name}] Connection failed: {e}")

async def main():
    await asyncio.gather(*(test_ws(name, uri) for name, uri in endpoints.items()))

asyncio.run(main())
