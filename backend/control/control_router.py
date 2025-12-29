# backend/control/control_router.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
from backend.utils.mqtt_client import MQTTClient
from backend.config import settings

router = APIRouter()
mqtt = MQTTClient()

class CommandPayload(BaseModel):
    command: str
    params: dict | None = None

@router.post("/drone/command")
async def drone_command(payload: CommandPayload):
    cmd = payload.command.lower()
    if cmd not in ["takeoff", "land", "rtl", "move"]:
        raise HTTPException(status_code=400, detail="Invalid command")
    msg = {"command": cmd, "params": payload.params or {}}
    mqtt.publish_command(settings.mqtt_topic_commands, json.dumps(msg))
    # Optionally return a server-side command id/ack
    return {"status":"sent", "command": msg}
