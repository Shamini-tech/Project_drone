# backend/utils/mqtt_client.py
import json
import threading
import time
import paho.mqtt.client as mqtt
from backend.config import settings
from backend.utils.shared_state import SharedState

_shared = SharedState()

class MQTTClient:
    def __init__(self, on_message_cb=None):
        self.client = mqtt.Client()
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message
        self.on_message_cb = on_message_cb
        self._connected = False

    def _on_connect(self, client, userdata, flags, rc):
        print("MQTT connected with rc", rc)
        self._connected = True
        client.subscribe(settings.mqtt_topic_telemetry)

    def _on_message(self, client, userdata, msg):
        try:
            payload = msg.payload.decode()
            data = json.loads(payload)
            # update shared state
            _shared.update_telemetry(data)
            if self.on_message_cb:
                self.on_message_cb(data)
        except Exception as e:
            print("MQTT on_message error:", e)

    def start(self):
        def _run():
            try:
                self.client.connect(settings.mqtt_broker, settings.mqtt_port, 60)
                self.client.loop_forever()
            except Exception as e:
                print("MQTT connect error:", e)
                time.sleep(5)
        t = threading.Thread(target=_run, daemon=True)
        t.start()

    def publish_command(self, command_topic, payload):
        try:
            self.client.publish(command_topic, payload)
        except Exception as e:
            print("MQTT publish error:", e)
