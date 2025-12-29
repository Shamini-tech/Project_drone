import cv2
import paho.mqtt.client as mqtt
import json
import time
import numpy as np
import tensorrt as trt
import pycuda.autoinit
import pycuda.driver as cuda

# ------------------------------
# Load TensorRT Engine
# ------------------------------
TRT_LOGGER = trt.Logger(trt.Logger.INFO)

def load_engine(path):
    with open(path, "rb") as f, trt.Runtime(TRT_LOGGER) as runtime:
        return runtime.deserialize_cuda_engine(f.read())

engine = load_engine("yolov5s.engine")
context = engine.create_execution_context()

# Allocate buffers
input_shape = (1, 3, 640, 640)
input_size = np.prod(input_shape)
output_size = engine.get_binding_shape(1)[1]

d_input = cuda.mem_alloc(input_size * np.float32().itemsize)
d_output = cuda.mem_alloc(output_size * np.float32().itemsize)

# Host buffers
h_input = cuda.pagelocked_empty(input_size, dtype=np.float32)
h_output = cuda.pagelocked_empty(output_size, dtype=np.float32)

# ------------------------------
# MQTT SETUP
# ------------------------------
client = mqtt.Client()
client.connect("backend-ip-here", 1883, 60)

# ------------------------------
# Pi Camera Capture (libcamera)
# ------------------------------
gst_pipeline = (
    "libcamera-vid -t 0 --inline --width 640 --height 480 "
    "--framerate 30 --codec mjpeg -o - | "
    "ffmpeg -i pipe:0 -f rawvideo -pix_fmt bgr24 pipe:1"
)

cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("ERROR: Could not open Pi Camera stream.")
    exit()

print("Camera stream OK. Starting inference...")

# ------------------------------
# MAIN LOOP
# ------------------------------
while True:
    ret, frame = cap.read()
    if not ret:
        continue

    img_resized = cv2.resize(frame, (640, 640))
    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    img_norm = img_rgb.astype(np.float32) / 255.0
    img_transpose = np.transpose(img_norm, (2, 0, 1))
    
    np.copyto(h_input, img_transpose.ravel())

    # Run TensorRT inference
    cuda.memcpy_htod(d_input, h_input)
    context.execute_v2([int(d_input), int(d_output)])
    cuda.memcpy_dtoh(h_output, d_output)

    # Parse detections
    detections = h_output.reshape(-1, 6)
    detected_objects = []

    for det in detections:
        x1, y1, x2, y2, conf, cls = det
        if conf < 0.5:
            continue
        detected_objects.append({
            "object": int(cls),
            "confidence": float(conf),
            "bbox": [float(x1), float(y1), float(x2), float(y2)]
        })

    # Publish alert
    payload = {
        "objects": detected_objects,
        "timestamp": time.time()
    }

    client.publish("drone/ai_alerts", json.dumps(payload))

