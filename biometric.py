import time
import json
import serial
import adafruit_fingerprint
from notifications import send_fingerprint_status
from gate import open_gate
from config import gate_config_list
import RPi.GPIO as GPIO


finger = None


def blinkled(pin):
    GPIO.setup(pin, GPIO.OUT)
    for i in range(2):
        GPIO.output(pin, GPIO.LOW)  # Turn on
        time.sleep(0.5)  # Sleep for 1 second
        GPIO.output(pin, GPIO.HIGH)  # Turn off
        time.sleep(0.5)  # Sleep for 1 second


def connect_sensor():
    global finger
    try:
        uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)
        finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)
        print("Connection with fingerprint sensor was established")
    except Exception as e:
        print(e)
        print("Connection with fingerprint sensor was not established")


connect_sensor()


def match_fingerprint(State):
    while State.mode == "ENTRY" and finger.get_image() != adafruit_fingerprint.OK:
        pass
    if State.mode == "ENROLL":
        return "ENROLL"
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False

    return finger.finger_id


def enroll_fingerprint(location, State):
    enrolled = False
    image = None
    message = ""

    for i in range(1, 3):
        if i == 1:
            print("Place finger on sensor...", end="")
            send_fingerprint_status("Place finger on sensor...", recipients=[
                                    State.notification_recipient])
        else:
            print("Place same finger again...", end="")
            send_fingerprint_status("Place same finger again...", recipients=[
                                    State.notification_recipient])

        while True and State.mode == "ENROLL":
            image = finger.get_image()
            if image == adafruit_fingerprint.OK:
                # print("Image taken")
                # send_fingerprint_status("Image taken", recipients=[State.notification_recipient])
                break
            if image == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif image == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                send_fingerprint_status("Imaging error", recipients=[
                                        State.notification_recipient])
                return False, location, image, "Imaging error"
            else:
                print("Other error")
                message = "Other error"
                send_fingerprint_status("Other error", recipients=[
                                        State.notification_recipient])
                return False, location, image, "Other error"

        # print("Templating...", end="")
        # send_fingerprint_status("Templating...", recipients=[State.notification_recipient])
        image = finger.image_2_tz(i)
        if image == adafruit_fingerprint.OK:
            pass
            # print("Templated")
            # send_fingerprint_status("Templated", recipients=[State.notification_recipient])
        else:
            if image == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
                send_fingerprint_status("Image too messy", recipients=[
                                        State.notification_recipient])
                message = 'Image too messy'
            elif image == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
                send_fingerprint_status("Could not identify features", recipients=[
                                        State.notification_recipient])
                message = 'Could not identify features'
            elif image == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
                send_fingerprint_status("Image invalid", recipients=[
                                        State.notification_recipient])
                message = 'Image Invalid'
            else:
                print("Other Error")
                send_fingerprint_status("Other Error", recipients=[
                                        State.notification_recipient])
                message = 'Other Error'
            return False, location, image, message

        if i == 1:
            print("Remove finger")
            send_fingerprint_status("Remove Finger", recipients=[
                                    State.notification_recipient])
            while image != adafruit_fingerprint.NOFINGER:
                image = finger.get_image()

    # print("Creating model...", end="")
    # send_fingerprint_status("Creating model...", recipients=[State.notification_recipient])
    image = finger.create_model()
    if image == adafruit_fingerprint.OK:
        pass
        # print("Created")
        # send_fingerprint_status("Created", recipients=[State.notification_recipient])
    else:
        if image == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
            send_fingerprint_status("Prints did not match", recipients=[
                                    State.notification_recipient])
            message = 'Prints did not match'
        else:
            print("Other error")
            send_fingerprint_status("Other error", recipients=[
                                    State.notification_recipient])
            message = 'Other Error'

        return False, location, image, message

    # print("Storing model #%d..." % location, end="")
    # send_fingerprint_status("Storing model", recipients=[State.notification_recipient])
    image = finger.store_model(location)
    if image == adafruit_fingerprint.OK:
        print("Fingerprint saved")
        send_fingerprint_status("Fingerprint saved", recipients=[
                                State.notification_recipient])
    else:
        if image == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
            send_fingerprint_status("Bad storage location", recipients=[
                                    State.notification_recipient])
            message = 'Bad storage location'
        elif image == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
            send_fingerprint_status("Flash storage error", recipients=[
                                    State.notification_recipient])
            message = 'Flash storage error'
        else:
            print("Other error")
            send_fingerprint_status("Other error", recipients=[
                                    State.notification_recipient])
            message = 'Other Error'
        return False, location, image, message

    return True, location, image, "Success"


def find_empty_location():
    finger.read_templates()
    for i in range(1, 128):
        if i not in finger.templates:
            return i
    return 1


def fingerprint_function(MQTTClient):
    if not finger:
        return

    fingerprint_function.stop = False

    class State:
        mode = "ENTRY"
        fingerprint_id = None
        notification_recipient = None

    def on_signal_recieved(client, userdata, message):
        nonlocal State
        print("yes")
        payload = json.loads(message.payload)
        State.mode = "ENROLL" if (payload.get(
            "mode", "ENTRY") == "ENROLL") else "ENTRY"
        State.notification_recipient = payload.get("expo_token", None)
        State.fingerprint_id = payload.get("fingerprint_id", None)

    MQTTClient.subscribe(topic="FINGERPRINT_SENSOR_MODE_CONTROL",
                         QoS=1, callback=on_signal_recieved)
    print("Subscribed to topic 'FINGERPRINT_SENSOR_MODE_CONTROL' ...")

    while not fingerprint_function.stop:
        try:
            if State.mode == "ENROLL":
                fingerprint_location = find_empty_location()
                enrolled, location, image, message = enroll_fingerprint(
                    fingerprint_location, State)

                if enrolled:
                    payload = json.dumps({
                        "fingerprint_id": State.fingerprint_id,
                        "fid": location,
                        "enrolled": True,
                    })
                    MQTTClient.publish(
                        topic="FINGERPRINT_REGISTRATION", payload=payload, QoS=1)

                else:
                    payload = json.dumps({
                        "fid": State.fingerprint_id,
                        "message": message,
                        "enrolled": False
                    })
                    MQTTClient.publish(
                        topic="FINGERPRINT_REGISTRATION", payload=payload, QoS=1)

                State.mode = "ENTRY"
                time.sleep(2)

            else:
                fid = match_fingerprint(State)
                if fid == "ENROLL":
                    pass
                elif fid:
                    print("Fingerprint found at location,", fid)
                    payload = json.dumps({"fid": fid})
                    open_gate(gate_id=1)
                    try:
                        MQTTClient.publish(
                            topic="FINGERPRINT_VALIDATION", QoS=1, payload=payload)
                    except Exception as e:
                        print(e)
                else:
                    blinkled(gate_config_list[1]['red_led_pin'])
                    print("Invalid Fingerprint")

        except Exception as e:
            print(e)
            connect_sensor()

    print(f"Stopped thread for fingerprint sensor")
