import RPi.GPIO as GPIO
import time
import json
from datetime import datetime, timedelta

GPIO.setmode(GPIO.BOARD)

def plant_control_function(MQTTClient, plant_config):

    plant_control_function.stop = False             # Function attribute used for stopping thread
    plant_id = plant_config["plant_id"]
    sms_pin = plant_config['sms_pin']         # Pin for taking sensor inputs
    output_pin = plant_config['output_pin']    # Pin for giving output for water pump motors
    GPIO.setup(sms_pin, GPIO.IN)
    GPIO.setup(output_pin, GPIO.OUT, initial=GPIO.HIGH)

    Mode_To_GPIO_Signal = {
        "ON": GPIO.LOW,
        "OFF": GPIO.HIGH,
    }

    class Mode:
        mode = "OFF"

    stop_motor_on = datetime.min
    cooldown = datetime.min

    pour_water_time = 2        # in seconds
    cooldown_time = 20          # in seconds

    def on_plant_signal_received(client, userdata, message):
        nonlocal Mode
        try:
            payload = json.loads(message.payload)
            Mode.mode = payload.get("mode", "AUTO")
            print(payload.get("message"))
        except Exception as err:
            print(f"Payload Object has an error.\nPayload: {payload}\nException Error: {err}")

    def auto_mode(sms_pin):
        nonlocal stop_motor_on, cooldown, pour_water_time, cooldown_time, plant_id, Mode_To_GPIO_Signal
        try:
            if stop_motor_on >= datetime.now():
                # print(f"PlantID {plant_id} Keeping motor on till time specified")
                return Mode_To_GPIO_Signal["ON"]

            if cooldown >= datetime.now():
                # print(f"PlantID {plant_id} On cooldown for {(cooldown-datetime.now()).total_seconds()} seconds")
                return Mode_To_GPIO_Signal["OFF"]

            if GPIO.input(sms_pin):
                # print(f"PlantID {plant_id} Water Inadequate, no cooldown period detected, pour water for {pour_water_time} seconds")
                stop_motor_on = datetime.now() + timedelta(seconds=pour_water_time)
                cooldown = stop_motor_on + timedelta(seconds=cooldown_time)
                return Mode_To_GPIO_Signal["ON"]

            else:
                # print(f"PlantID {plant_id} Water Adequate")
                return Mode_To_GPIO_Signal["OFF"]

        except Exception as err:
            print("Exception:", err)

        return Mode_To_GPIO_Signal["OFF"]

    MQTTClient.subscribe(topic=f"PLANT_MODE_CONTROL/{plant_config['plant_id']}", QoS=1, callback=on_plant_signal_received)
    print("Subscribed to topic 'PLANT_MODE_CONTROL' ...")

    while not plant_control_function.stop:
        if Mode.mode == "AUTO":
            GPIO.output(output_pin, auto_mode(sms_pin))

        elif Mode.mode == "ON":
            GPIO.output(output_pin, Mode_To_GPIO_Signal["ON"])
        
        elif Mode.mode == "OFF":
            GPIO.output(output_pin, Mode_To_GPIO_Signal["OFF"])

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
