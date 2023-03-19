import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import json


def rfid_function(MQTTClient):
    rfid_function.stop = False
    mode = "READ"
    vehicle_id = None
    sensor = SimpleMFRC522()

    def on_register_mode(client, userdata, message):
        nonlocal mode, vehicle_id
        mode = "REGISTER"
        data = json.loads(message.payload)
        vehicle_id = data.get("vehicle_id")
    MQTTClient.subscribe(topic=f"RFID_MODE_CONTROL", QoS=0, callback=on_register_mode)


    while not rfid_function.stop:
        rfid, text = sensor.read()
        if mode == "REGISTER":
            payload = json.dumps({
                "rfid": rfid,
                "vehicle_id": vehicle_id,
            })
            MQTTClient.publish(topic="RFID_REGISTRATION", payload=payload)
            mode = "READ"
        else:
            payload = json.dumps({
                "rfid": rfid,
            })
            MQTTClient.publish(topic="RFID_VALIDATION", payload=payload)
        time.sleep(5)
