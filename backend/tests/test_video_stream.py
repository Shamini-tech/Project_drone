# test_video_stream.py
import asyncio
import base64
import json
import websockets
import requests

VIDEO_FRAME_B64 = None

def load_sample_frame_b64(path="sample.jpg"):
    with open(path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    return "data:image/jpeg;base64," + b64

async def ws_listen_video():
    uri = "ws://localhost:8000/ws/video"
    async with websockets.connect(uri) as ws:
        print("Connected to video WS")
        # receive one frame
        msg = await ws.recv()
        print("Received video message, length:", len(msg))

if __name__ == "__main__":
    FRAME = load_sample_frame_b64("sample.jpg")
    r = requests.post("http://localhost:8000/video/frame", json={"frame_b64": FRAME})
    print("POST frame:", r.status_code, r.text)
    asyncio.run(ws_listen_video())
