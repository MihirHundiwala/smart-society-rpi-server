import time
import serial
import adafruit_fingerprint


uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)


def match_fingerprint():
    while finger.get_image() != adafruit_fingerprint.OK:
        pass
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    return True


def finger_print_function(MQTTClient):
    finger_print_function.stop = False

    while not finger_print_function.stop:
        if match_fingerprint():
            payload = {
                "message" : f"Fingerprint matched, gate is open !",
            }
            MQTTClient.publish(topic = "GATE_CONTROL", payload = payload, QoS = 1)
        else:
            print("Invalid")


