import cv2, base64, time, json
import paho.mqtt.client as mqtt
from sim_camera import get_frame

client = mqtt.Client()
client.connect("localhost", 1883)

def encode_frame(frame):
    _, buffer = cv2.imencode('.jpg', frame)
    return base64.b64encode(buffer).decode()

distance = 10.0

for frame in get_frame():
    distance = max(0, distance - 0.05)  # simulate approaching cargo
    alert = "CARGO NEARBY" if distance < 3 else "OK"

    message = {
        "drone_id": "DRONE001",
        "distance": round(distance, 2),
        "alert": alert,
        "timestamp": time.time(),
        "frame": encode_frame(frame)
    }
    client.publish("drone/feed", json.dumps(message))
    time.sleep(0.1)
