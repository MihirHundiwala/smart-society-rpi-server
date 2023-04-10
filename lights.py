import RPi.GPIO as GPIO
import time
import json


def light_control_function(MQTTClient, light_config):
    # Function attribute used for stopping thread
    light_control_function.stop = False

    class Mode:
        mode = "AUTO"
    
    Mode_To_GPIO_Signal = {
        "ON": GPIO.LOW,
        "OFF": GPIO.HIGH,
    }

    # Pin for taking sensor inputs
    ldr_pin = int(light_config['ldr_pin'])
    output_pin = int(light_config['output_pin'])
    GPIO.setup(output_pin, GPIO.OUT)

    def auto_mode(ldr_pin):
        nonlocal Mode_To_GPIO_Signal
        try:
            count = 0
            GPIO.setup(ldr_pin, GPIO.OUT)
            GPIO.output(ldr_pin, GPIO.LOW)
            time.sleep(0.1)
            GPIO.setup(ldr_pin, GPIO.IN)

            while (GPIO.input(ldr_pin) == GPIO.LOW):
                count += 1

            # print(f"Sensor Output({light_config['light_id']}): {count}")
            if count < light_config["threshold"]:
                return Mode_To_GPIO_Signal["OFF"]
            else:
                return Mode_To_GPIO_Signal["ON"]

        except Exception as err:
            print("Error while receiving input from sensor.\n Exception:", err)

        return Mode_To_GPIO_Signal["ON"]    

    
    def on_light_signal_received(client, userdata, message):
        nonlocal Mode
        try:
            payload = json.loads(message.payload)
            Mode.mode = payload.get("mode", "AUTO")
            print(payload.get("message"))
        except Exception as err:
            print(f"Payload Object has an error.\nPayload: {payload}\nException Error: {err}")

    MQTTClient.subscribe(topic=f"LIGHT_MODE_CONTROL/{light_config['light_id']}", QoS=1, callback=on_light_signal_received)
    print("Subscribed to topic 'LIGHT_MODE_CONTROL' ...")

    while not light_control_function.stop:
        if Mode.mode == "AUTO":
            GPIO.output(output_pin, auto_mode(ldr_pin))
        elif Mode.mode == "ON":
            GPIO.output(output_pin, Mode_To_GPIO_Signal["ON"])
            # print("ON")
        elif Mode.mode == "OFF":
            GPIO.output(output_pin, Mode_To_GPIO_Signal["OFF"])

    print(f"Stopped thread for light-{light_config['light_id']}")
