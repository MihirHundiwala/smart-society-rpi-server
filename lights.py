import RPi.GPIO as GPIO
import time
import json


def light_control_function(MQTTClient, light_config):
    Mode_To_GPIO_Signal = {
        "ON": GPIO.LOW,
        "OFF": GPIO.HIGH,
    }
    # Function attribute used for stopping thread
    light_control_function.stop = False

    # Pin for taking sensor inputs
    ldr_pin = int(light_config['ldr_pin'])
    output_pin = int(light_config['output_pin'])
    GPIO.setup(output_pin, GPIO.OUT, initial=Mode_To_GPIO_Signal["OFF"])

    updated_mode = "AUTO"                       # Default
    current_mode = "AUTO"

    def on_light_signal_received(client, userdata, message):
        nonlocal updated_mode
        try:
            payload = json.loads(message.payload)
            updated_mode = payload.get("mode", "AUTO")
            print(payload.get("message"))
        except Exception as err:
            print(f"Payload Object has an error.\nPayload: {payload}\nException Error: {err}")

    def auto_mode(ldr_pin):
        try:
            count = 0
            GPIO.setup(ldr_pin, GPIO.OUT)
            GPIO.output(ldr_pin, GPIO.LOW)
            time.sleep(0.1)
            GPIO.setup(ldr_pin, GPIO.IN)

            while (GPIO.input(ldr_pin) == GPIO.LOW):
                count += 1

            print(f"Sensor Output for AUTO mode({light_config['light_id']}): {count}")
            if count < light_config["threshold"]:
                return Mode_To_GPIO_Signal["OFF"]
            else:
                return Mode_To_GPIO_Signal["ON"]

        except Exception as err:
            print("Error while receiving input from sensor.\n Exception:", err)

        return Mode_To_GPIO_Signal["ON"]

    MQTTClient.subscribe(
        topic=f"LIGHT_MODE_CONTROL/{light_config['light_id']}", QoS=0, callback=on_light_signal_received)
    print("Subscribed to topic 'LIGHT_MODE_CONTROL' ...")

    while not light_control_function.stop:
        if updated_mode == "AUTO":
            current_mode = "AUTO"
            GPIO.output(output_pin, auto_mode(ldr_pin))

        elif current_mode != updated_mode:
            current_mode = updated_mode
            GPIO.output(output_pin, Mode_To_GPIO_Signal[current_mode])

    print(f"Stopped thread for light-{light_config['light_id']}")
