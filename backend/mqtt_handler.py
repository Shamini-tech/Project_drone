import json
import paho.mqtt.client as mqtt
from utils.shared_state import telemetry_data, alert_data, video_frame_b64 


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload.decode())

    if topic == "drone/telemetry":
        telemetry_data.update(payload)

    elif topic == "drone/ai_alerts":
        alert_data.update(payload)

    elif topic == "drone/video":
        global video_frame_b64
        video_frame_b64 = payload["frame"]

def start_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect("mosquitto", 1883, 60)

    client.subscribe("drone/telemetry")
    client.subscribe("drone/ai_alerts")
    client.subscribe("drone/video")

    client.loop_start()
