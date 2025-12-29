# test_mqtt_flow.py
import paho.mqtt.client as mqtt
import json
c = mqtt.Client()
c.connect("localhost",1883,60)
payload = {"gps_lat": 12.34, "gps_lon": 56.78, "battery": 87}
c.publish("drone/telemetry", json.dumps(payload))
print("Published telemetry")
    