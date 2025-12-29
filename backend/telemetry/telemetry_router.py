# backend/telemetry/telemetry_router.py
from fastapi import APIRouter
from pydantic import BaseModel
from backend.utils.shared_state import get_shared_state

router = APIRouter()
shared = get_shared_state()

class TelemetryPayload(BaseModel):
    gps_lat: float | None = None
    gps_lon: float | None = None
    altitude: float | None = None
    battery: float | None = None
    speed: float | None = None

@router.post("/telemetry")
async def post_telemetry(payload: TelemetryPayload):
    shared.update_telemetry(payload.dict(exclude_none=True))
    return {"status":"ok"}
