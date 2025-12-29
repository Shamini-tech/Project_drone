# backend/ai/alert_engine.py
from backend.ai.postprocess import to_alerts
from datetime import datetime

def make_alert(detections):
    alert_type = to_alerts(detections)
    return {
        "type": alert_type,
        "detections": detections,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
