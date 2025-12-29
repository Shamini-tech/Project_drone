from fastapi import FastAPI
from fastapi.responses import JSONResponse
from mqtt_handler import start_mqtt, latest_frame


app = FastAPI()
start_mqtt()

@app.get("/api/telemetry")
def get_telemetry():
    return JSONResponse(latest_frame)
