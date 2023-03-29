import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from gate import open_gate
import time
import json

sensor = None
try:
    sensor = SimpleMFRC522()
    print("Connection with RFID reader was established")
except:
    print("Connection with RFID reader was not established")


def rfid_function(MQTTClient):
    global sensor
    if not sensor:
        return
    
    rfid_function.stop = False

    class State:
        mode = "ENTRY"
        vehicle_id = None
        notification_recipient = None

    def on_signal_recieved(client, userdata, message):
        nonlocal State
        payload = json.loads(message.payload)
        State.mode =  "ENROLL" if (payload.get("mode", "ENTRY") == "ENROLL") else "ENTRY"
        State.notification_recipient = payload.get("expo_token", None)
        State.vehicle_id = payload.get("vehicle_id", None)

    MQTTClient.subscribe(topic=f"RFID_MODE_CONTROL", QoS=0, callback=on_signal_recieved)
    print("Subscribed to topic 'RFID_MODE_CONTROL' ...")

    while not rfid_function.stop:
        try:
            rfid, text = sensor.read()
            print(rfid)
        except Exception as e:
            print(e)
            continue

        if State.mode == "ENROLL":
            if rfid:
                payload = json.dumps({
                    "rfid": rfid,
                    "vehicle_id": State.vehicle_id,
                    "enrolled": True,
                })
                MQTTClient.publish(topic="RFID_REGISTRATION", payload=payload, QoS=1)
            
            else:
                payload = json.dumps({
                    "vehicle_id": State.vehicle_id,
                    "enrolled": False,
                })
                MQTTClient.publish(topic="RFID_REGISTRATION", payload=payload, QoS=1)
        
            State.mode = "ENTRY"

        else:
            payload = json.dumps({
                "rfid": rfid,
            })
            # print("I am here")
            open_gate(gate_id=2, MQTTClient=MQTTClient, payload=payload, topic="RFID_VALIDATION")
            # MQTTClient.publish(topic="RFID_VALIDATION", QoS=1, payload=payload)
            # print("here 2")
        
        time.sleep(2)

    print(f"Stopped thread for rfid sensor")
    
