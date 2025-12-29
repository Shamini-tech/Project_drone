# backend/config.py
from pydantic import BaseSettings

class Settings(BaseSettings):
    mqtt_broker: str = "localhost"
    mqtt_port: int = 1883
    mqtt_topic_telemetry: str = "drone/telemetry"
    mqtt_topic_commands: str = "drone/commands"
    ws_video_path: str = "/ws/video"
    ws_alerts_path: str = "/ws/alerts"
    ws_telemetry_path: str = "/ws/telemetry"

settings = Settings()
