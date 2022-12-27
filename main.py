import threading
import RPi.GPIO as GPIO
from aws.connections import MQTTClient
from lights.functions import led_control_function
from lights.led_configs import led_config_list

# _____________________________________________________

print("Setting up Raspberry PI...")
GPIO.setmode(GPIO.BOARD)

# _____________________________________________________

print('Initiating Realtime Data Transfer From Raspberry Pi To AWS IoT Core...')
MQTTClient.connect()

# _____________________________________________________

thread_list = []

# _____________________________________________________

for led_config in led_config_list:
    thread = threading.Thread(
        target=led_control_function, 
        name=f"thread-led-{led_config['led_id']}", 
        args=(MQTTClient, led_config)
    )
    thread_list.append(thread)
    print(f"Starting thread for lights [LED-{led_config['led_id']}]...") 
    thread.start()

# _____________________________________________________

try:
    while True:
        pass

except KeyboardInterrupt:
    for thread in thread_list:
        thread.target.stop = True
        thread.join()

finally:
    print("Cleaning GPIO")
    GPIO.cleanup()
    print("Shutting down server...")

# _____________________________________________________
