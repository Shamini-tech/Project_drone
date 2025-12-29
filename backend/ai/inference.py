# backend/ai/inference.py
import cv2
import base64
import numpy as np
from backend.ai.yolo_engine import load_model, run_inference
from backend.ai.alert_engine import make_alert

# Global model instance (loaded once by server)
MODEL = load_model()

def b64_to_image(b64str):
    header, _, data = b64str.partition(',')
    decoded = base64.b64decode(data or header)
    arr = np.frombuffer(decoded, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img

def infer_from_b64(b64str):
    img = b64_to_image(b64str)
    if img is None:
        raise ValueError("Could not decode image")
    detections = run_inference(MODEL, img)
    alert = make_alert(detections)
    # return detection and optionally annotated image (as bytes)
    return detections, alert, img
