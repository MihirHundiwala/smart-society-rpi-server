import RPi.GPIO as GPIO
import time
import json
from datetime import datetime, timedelta


def plant_control_function(MQTTClient, plant_config):

    plant_control_function.stop = False             # Function attribute used for stopping thread

    sms_pin = int(plant_config['sms_pin'])          # Pin for taking sensor inputs
    output_pin = int(plant_config['output_pin'])    # Pin for giving output for water pump motors
    GPIO.setup(sms_pin, GPIO.IN)
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)

    updated_mode = "AUTO"                           # Default
    current_mode = "AUTO"

    Mode_To_GPIO_Signal = {
        "ON": GPIO.LOW,
        "OFF": GPIO.HIGH,
    }

    stop_motor_on = datetime.min
    cooldown = datetime.min

    pour_water_time = 5         # in seconds
    cooldown_time = 20          # in seconds

    def on_plant_signal_received(client, userdata, message):
        nonlocal updated_mode
        try:
            payload = json.loads(message.payload)
            updated_mode = payload.get("mode", "AUTO")
            print(payload.get("message"))
        except Exception as err:
            print(
                f"Payload Object has an error.\nPayload: {payload}\nException Error: {err}")

    def auto_mode(sms_pin):
        nonlocal stop_motor_on, cooldown, pour_water_time, cooldown_time
        try:
            if stop_motor_on >= datetime.now():
                print("Keeping motor on till time specified")
                return GPIO.LOW

            if cooldown >= datetime.now():
                print(
                    f"On cooldown for {(cooldown-datetime.now()).total_seconds()} seconds")
                return GPIO.HIGH

            elif GPIO.input(sms_pin):
                print(
                    f"Water Inadequate, no cooldown period detected, pour water for {pour_water_time} seconds")
                stop_motor_on = datetime.now() + timedelta(seconds=pour_water_time)
                cooldown = stop_motor_on + timedelta(seconds=cooldown_time)
                return GPIO.LOW

            else:
                print("Water Adequate")
                return GPIO.HIGH

        except Exception as err:
            print(
                "Error while receiving input from soil moisture sensor.\n Exception:", err)

        return GPIO.HIGH

    MQTTClient.subscribe(
        topic=f"PLANT_MODE_CONTROL/{plant_config['plant_id']}", QoS=0, callback=on_plant_signal_received)
    print("Subscribed to topic 'PLANT_MODE_CONTROL' ...")

    while not plant_control_function.stop:
        if updated_mode == "AUTO":
            current_mode = "AUTO"
            GPIO.output(output_pin, auto_mode(sms_pin))

        elif current_mode != updated_mode:
            current_mode = updated_mode
            GPIO.output(output_pin, Mode_To_GPIO_Signal[current_mode])
            
        time.sleep(1)

    print(f"Stopped thread for plant-{plant_config['plant_id']}")


# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(8,GPIO.IN)
# GPIO.setup(10,GPIO.OUT)

# while True:
#     if (GPIO.input(8)):
#         print("Water Inadequate")
#         GPIO.output(10,GPIO.HIGH)
#     else:
#         print("Water Adequate")
#         GPIO.output(10,GPIO.LOW)
#     time.sleep(2)
