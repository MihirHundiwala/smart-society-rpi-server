import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import json

def rfid_function(MQTTClient):
    rfid_function.stop = False

    reader = SimpleMFRC522()
    while not rfid_function.stop:
        id, text = reader.read()
        payload = json.dumps({
            "message" : f"RFID tag matched, gate is open !",
        })
        MQTTClient.publish(topic = "GATE_CONTROL", payload = payload, QoS = 1)
        time.sleep(5)