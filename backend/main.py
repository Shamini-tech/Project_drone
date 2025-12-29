# backend/main.py
import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# REST routers
from backend.video.video_router import router as video_router
from backend.control.control_router import router as control_router
from backend.telemetry.telemetry_router import router as telemetry_router


# WebSocket routers
from backend.video.video_ws import router as video_ws_router
from backend.video.alerts_ws import router as alerts_ws_router
from backend.telemetry.telemetry_ws import router as telemetry_ws_router

# Background tasks
from backend.video.stream_processor import video_consumer_loop
from backend.utils.mqtt_client import MQTTClient

app = FastAPI(title="Drone Backend")

# Allow all CORS (adjust for production if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register REST routers
app.include_router(video_router)
app.include_router(control_router)
app.include_router(telemetry_router)

# Register WebSocket routers
app.include_router(video_ws_router)
app.include_router(alerts_ws_router)
app.include_router(telemetry_ws_router)

# Health endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}

# Startup events
@app.on_event("startup")
async def startup_event():
    # Start MQTT client
    mqtt = MQTTClient()
    mqtt.start()

    # Start video consumer loop
    loop = asyncio.get_event_loop()
    loop.create_task(video_consumer_loop())
    print("Startup finished")

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=False)
