import time
import json
import cv2
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect("localhost", 1883, 60)

while True:
    # Send telemetry
    telemetry = {
        "battery": 87,
        "distance": 42,
        "status": "FLYING"
    }
    client.publish("drone/telemetry", json.dumps(telemetry))

    # Send alerts
    alerts = {
        "alert": "NORMAL"
    }
    client.publish("drone/alerts", json.dumps(alerts))

    time.sleep(1)
