import time, json
import serial
import adafruit_fingerprint


uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)
finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

finger.empty_library()

def match_fingerprint(Mode):
    while Mode.mode == "ENTRY" and finger.get_image() != adafruit_fingerprint.OK:
        pass
    if Mode.mode == "ENROLL":
        return "ENROLL"
    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
        return False
    if finger.finger_search() != adafruit_fingerprint.OK:
        return False
    
    return finger.finger_id


def enroll_fingerprint(location):
    enrolled = False
    image = None
    message = ""

    for i in range(1, 3):
        if i == 1:
            print("Place finger on sensor...")
        else:
            print("Place same finger again...")

        while True:
            image = finger.get_image()
            if image == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if image == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif image == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False, location, image, "Imaging error"
            else:
                print("Other error")
                message = "Other error"
                return False, location, image, "Other error"

        print("Templating...", end="")
        image = finger.image_2_tz(i)
        if image == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if image == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
                message = 'Image too messy'
            elif image == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
                message = 'Could not identify features'
            elif image == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
                message = 'Image Invalid'
            else:
                print("Other Error")
                message = 'Other Error'
            return False, location, image, message

        if i == 1:
            print("Remove finger")
            time.sleep(1)
            while image != adafruit_fingerprint.NOFINGER:
                image = finger.get_image()

    print("Creating model...", end="")
    image = finger.create_model()
    if image == adafruit_fingerprint.OK:
        print("Created")
    else:
        if image == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
            message = 'Prints did not match'
        else:
            print("Other error")
            message = 'Other Error'

        return False, location, image, message

    print("Storing model #%d..." % location, end="")
    image = finger.store_model(location)
    if image == adafruit_fingerprint.OK:
        print("Stored")
    else:
        if image == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
            message = 'Bad storage location'
        elif image == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
            message = 'Flash storage error'
        else:
            print("Other error")
            message = 'Other Error'
        return False, location, image, message

    return True, location, image, "Success" 


def find_empty_location():
    finger.read_templates()
    for i in range(1,128):
        print(i)
        if i not in finger.templates:
            return i
    return 1


def fingerprint_function(MQTTClient):
    fingerprint_function.stop = False

    class Mode:
        mode = "ENTRY"

    fingerprint_id = None

    def on_enroll_signal_recieved(client, userdata, message):
        nonlocal Mode, fingerprint_id
        Mode.mode = "ENROLL"
        payload = json.loads(message.payload)
        fingerprint_id = payload.get("fingerprint_id")
    MQTTClient.subscribe(topic="FINGERPRINT_ENROLL", QoS=1, callback=on_enroll_signal_recieved)
    print("Subscribed to topic 'FINGERPRINT_ENROLL' ...")


    while not fingerprint_function.stop:
        if Mode.mode == "ENROLL":
            enrolled, location, image, message = enroll_fingerprint(find_empty_location())

            if enrolled:
                payload = json.dumps({
                    "fingerprint_id": fingerprint_id,
                    "fid": location,
                    "enrolled": True,
                })
                MQTTClient.publish(topic = "FINGERPRINT_REGISTRATION", payload = payload, QoS = 1)

            else:
                payload = json.dumps({
                    "fid" : fingerprint_id,
                    "enrolled": False,
                    "message": message
                })
                MQTTClient.publish(topic = "FINGERPRINT_REGISTRATION", payload = payload, QoS = 1)

            Mode.mode = "ENTRY"

        else:
            fid = match_fingerprint(Mode)
            if fid == "ENROLL":
                pass
            elif fid:
                payload = json.dumps({"fid":fid})
                MQTTClient.publish(topic = "FINGERPRINT_VALIDATION", payload = payload, QoS = 1)
            else:
                print("Invalid Fingerprint")
        time.sleep(3)

    print(f"Stopped thread for fingerprint sensor")
