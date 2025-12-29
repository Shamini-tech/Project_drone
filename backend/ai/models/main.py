import time
import cv2
import numpy as np
import requests
from ultralytics import YOLO
import torch

# ---------- SETTINGS ----------
ALERT_URL = "http://127.0.0.1:5000/alert"  # Local web server
MAX_DISTANCE_M = 20                        # Danger zone distance
CAMERA_INDEX = 0                           # Default laptop webcam
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Distance estimation method: "depth", "hybrid" (recommended - most accurate), or "size"
# "hybrid" combines depth + object size for better accuracy
DISTANCE_METHOD = "hybrid"  # Change to "depth" for depth-only, "size" for size-only
# --------------------------------

print("Loading models...")

# YOLOv8 Nano (auto-download)
yolo = YOLO("yolov8n.pt")
yolo.model.to(DEVICE)

# MiDaS Small depth estimator (auto-download)
midas = torch.hub.load("intel-isl/MiDaS", "MiDaS_small")
midas.to(DEVICE).eval()

midas_transform = torch.hub.load("intel-isl/MiDaS", "transforms").small_transform

print("Models loaded.")


# ------------ DEPTH ESTIMATION -------------
def get_depth_map(frame):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    input_batch = midas_transform(img).to(DEVICE)

    with torch.no_grad():
        prediction = midas(input_batch)

        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False
        ).squeeze()

    depth_map = prediction.cpu().numpy()
    return depth_map


# ------------ CALIBRATION FUNCTION ----------
# Calibrated values from calibrate.py (using inverse relationship: 1/rel_depth)
# Latest calibration with 4-5 images
K_FACTOR = 520.4022218157677
OFFSET   = 0.2361134142753181

# Correction factor: Adjust this if distances are consistently off
# If 3m shows as 1.8m, try DISTANCE_CORRECTION = 1.67 (3.0 / 1.8)
# If distances are too large, use a value < 1.0 (e.g., 0.8)
DISTANCE_CORRECTION = 1.0  # Start with 1.0, adjust based on testing


def depth_to_meters(rel_depth):
    if rel_depth <= 0:
        return 999
    # Calculate distance using calibration formula (inverse relationship)
    # This matches calibrate.py: distance = OFFSET + K_FACTOR * (1/rel_depth)
    inv_depth = 1.0 / rel_depth
    dist_m = K_FACTOR * inv_depth + OFFSET
    # Apply correction factor
    dist_m = dist_m * DISTANCE_CORRECTION
    # Clamp to reasonable range (0.1m to 200m)
    return max(0.1, min(dist_m, 200))


# Median depth from bounding box
def median_depth(depth_map, box):
    x1, y1, x2, y2 = map(int, box)
    patch = depth_map[y1:y2, x1:x2]
    if patch.size == 0:
        return 999
    return float(np.median(patch))


# ------------ OBJECT SIZE-BASED DISTANCE (More accurate for known objects) ----------
# Typical real-world heights in meters for common objects
OBJECT_HEIGHTS = {
    "person": 1.7,
    "bicycle": 1.2,
    "car": 1.5,
    "motorcycle": 1.3,
    "airplane": 3.0,
    "bus": 3.0,
    "train": 3.5,
    "truck": 2.5,
    "boat": 2.0,
    "bird": 0.3,
    "cat": 0.3,
    "dog": 0.5,
    "horse": 1.6,
    "sheep": 0.8,
    "cow": 1.4,
    "elephant": 3.0,
    "bear": 1.5,
    "zebra": 1.5,
    "giraffe": 5.0,
}

# Approximate focal length for typical webcam (in pixels)
# To calibrate: Measure a person at known distance (e.g., 2m), note their pixel height
# Then: FOCAL_LENGTH_PX = (person_height_px * 2.0) / 1.7
# Typical values: 600 for 720p, 800 for 1080p webcam
FOCAL_LENGTH_PX = 600  # Adjust this for better size-based accuracy


def distance_from_size(box, label, frame_height):
    """Estimate distance using object size (very accurate for known objects)."""
    x1, y1, x2, y2 = map(int, box)
    box_height_px = y2 - y1
    
    # Get typical height for this object type
    real_height = OBJECT_HEIGHTS.get(label.lower(), None)
    if real_height is None:
        return None  # Unknown object type
    
    # Distance formula: distance = (real_height * focal_length) / pixel_height
    if box_height_px > 0:
        distance = (real_height * FOCAL_LENGTH_PX) / box_height_px
        return max(0.5, min(distance, 100))  # Clamp between 0.5m and 100m
    return None


def hybrid_distance(depth_dist, size_dist, label):
    """Combine depth and size estimates for better accuracy."""
    if size_dist is None:
        # No size estimate available, use depth only
        return depth_dist
    
    # Weighted average: trust size more for known objects, depth for unknown
    # Size is usually more accurate for people, cars, etc.
    if label.lower() in OBJECT_HEIGHTS:
        # For known objects, weight size more (70% size, 30% depth)
        return 0.7 * size_dist + 0.3 * depth_dist
    else:
        # For unknown objects, use depth only
        return depth_dist


# Send alert
def send_alert(name, dist):
    data = {
        "timestamp": time.time(),
        "object": name,
        "distance_m": round(dist, 2)
    }
    try:
        requests.post(ALERT_URL, json=data, timeout=1)
    except Exception:
        # Server might be offline; ignore to keep loop running
        pass


# ------------------- MAIN LOOP -------------------
cap = cv2.VideoCapture(CAMERA_INDEX)
print("Starting video stream...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO detection
    detections = yolo.predict(frame, device=DEVICE, conf=0.35)[0]

    # Depth map (only if using depth or hybrid method)
    if DISTANCE_METHOD in ["depth", "hybrid"]:
        depth_map = get_depth_map(frame)

    # For each detected object
    for box, cls in zip(detections.boxes.xyxy.cpu().numpy(),
                        detections.boxes.cls.cpu().numpy()):

        label = yolo.model.names[int(cls)]

        # Calculate distance based on selected method
        if DISTANCE_METHOD == "hybrid":
            # Hybrid: Combine depth + object size for best accuracy
            rel = median_depth(depth_map, box)
            depth_dist = depth_to_meters(rel)
            size_dist = distance_from_size(box, label, frame.shape[0])
            dist_m = hybrid_distance(depth_dist, size_dist, label)
        elif DISTANCE_METHOD == "size":
            # Size-based only (no calibration needed)
            dist_m = distance_from_size(box, label, frame.shape[0])
            if dist_m is None:
                continue  # Skip if object type unknown
        else:
            # Depth-based only (original method)
            rel = median_depth(depth_map, box)
            dist_m = depth_to_meters(rel)
        
        # Debug: print all detections to see the pattern
        if DISTANCE_METHOD == "hybrid":
            size_str = f"{size_dist:.2f}m" if size_dist is not None else "N/A"
            print(f"DEBUG: {label} - depth={depth_dist:.2f}m, size={size_str}, hybrid={dist_m:.2f}m")
        else:
            print(f"DEBUG: {label} - dist={dist_m:.2f}m")

        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"{label} {dist_m:.1f}m",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )

        # Trigger warning
        if dist_m <= MAX_DISTANCE_M:
            print(f"WARNING: {label} at {dist_m:.2f}m")
            send_alert(label, dist_m)

    cv2.imshow("Drone Vision", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

