import time
import RPi.GPIO as GPIO 

def gate_control_function(MQTTClient):
    gate_control_function.stop = False # Function attribute used for stopping thread

    def blinkled(client, userdata, message):
        # Set pin 36 to be an output pin and set initial value to low (off)
        print("Blinking")
        GPIO.setup(36, GPIO.OUT)
        for i in range(5):
            GPIO.output(36, GPIO.HIGH)  # Turn on
            time.sleep(0.5)  # Sleep for 1 second
            GPIO.output(36, GPIO.LOW)  # Turn off
            time.sleep(0.5)  # Sleep for 1 second

    print("Subscribing to topic 'GATE_CONTROL' ...")
    MQTTClient.subscribe(topic="GATE_CONTROL", QoS=0, callback=blinkled)
