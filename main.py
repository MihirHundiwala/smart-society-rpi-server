import threading
from aws.connections import MQTTClient
import RPi.GPIO as GPIO

from gate import gate_control_function

from lights import light_control_function
from config import light_config_list

from plants import plant_control_function
from config import plant_config_list


# _____________________________________________________

print("Setting up Raspberry PI...")
GPIO.setmode(GPIO.BOARD)

# _____________________________________________________

print('Initiating Realtime Data Transfer From Raspberry Pi To AWS IoT Core...')
MQTTClient.connect()

# _____________________________________________________

thread_list = []

# _____________________________________________________

for light_config in light_config_list:
    thread = threading.Thread(
        target=light_control_function,
        name=f"thread-light-{light_config['light_id']}",
        args=(MQTTClient, light_config)
    )
    thread_list.append(thread)
    thread.start()
    print(f"Started thread for lights [light-{light_config['light_id']}]...")

# _____________________________________________________

for plant_config in plant_config_list:
    thread = threading.Thread(
        target=plant_control_function,
        name=f"thread-plant-{plant_config['plant_id']}",
        args=(MQTTClient, plant_config)
    )
    thread_list.append(thread)
    thread.start()
    print(f"Started thread for plants [plant-{plant_config['plant_id']}]...")

# _____________________________________________________

gate_thread = threading.Thread(
    target=gate_control_function,
    name="thread-gate-control",
    args=(MQTTClient,)
)
gate_thread.start()
thread_list.append(gate_thread)
print("Started thread for gate")

_____________________________________________________

try:
    while True:
        pass

except KeyboardInterrupt:
    light_control_function.stop = True
    plant_control_function.stop = True
    gate_control_function.stop = True
    for thread in thread_list:
        thread.join()

finally:
    print("Cleaning GPIO")
    GPIO.cleanup()
    print("Shutting down server...")

# _____________________________________________________
