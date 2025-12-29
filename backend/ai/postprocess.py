# backend/ai/postprocess.py
def to_alerts(detections):
    """
    detections: list of dicts {label, confidence, bbox}
    returns: alert string
    """
    labels = {d['label'].lower() for d in detections}
    if 'person' in labels:
        return "PERSON_DETECTED"
    if 'car' in labels or 'vehicle' in labels:
        return "VEHICLE_DETECTED"
    if 'fire' in labels or 'smoke' in labels:
        return "FIRE_DETECTED"
    return "NO_THREAT"
