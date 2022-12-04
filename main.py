import threading
import RPi.GPIO as GPIO
from .AWSIoT import MQTTClient
from .lights import lights_main


# SETUP
print("Setting up Raspberry PI...")
GPIO.setmode(GPIO.BOARD)

print('Initiating Realtime Data Transfer From Raspberry Pi To AWS IoT Core...')
MQTTClient.connect()

thread_lights = threading.Thread(target=lights_main, name='thread-lights', args=(MQTTClient,))
print("Starting thread for lights...")
thread_lights.start()


try:
    while True:
        pass

except KeyboardInterrupt:
    lights_main.stop = True
    thread_lights.join()

finally:
    print("Cleaning GPIO")
    GPIO.cleanup()


print("Shutting down server...")