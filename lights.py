import json
import time
import RPi.GPIO as GPIO

def lights_main(MQTTClient):

    lights_main.stop = False    # Function attribute used for stopping thread
    ldr_pin = 11                # Pin for taking sensor inputs
    output_pin = 40
    updated_mode = "AUTO"       # Default
    current_mode = updated_mode
    Mode_To_GPIO_Signal = {
        "ON": GPIO.HIGH,
        "OFF": GPIO.LOW,
    }

    GPIO.setup(output_pin, GPIO.OUT)


    def on_LED_signal_received(client, userdata, message):
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

            print("Sensor Output for AUTO mode:", count)
            if count < 79999: return GPIO.LOW
            else: return GPIO.HIGH

        except Exception as err:
            print("Error while receiving input from sensor.\n Exception:", err)


    print("Subscribing to topic 'Manual_LED_Control' ...")
    MQTTClient.subscribe(topic="Manual_LED_Control", QoS=0, callback=on_LED_signal_received)


    while not lights_main.stop:
        if updated_mode == "AUTO":
            current_mode = "AUTO"
            GPIO.output(output_pin, auto_mode(ldr_pin))

        elif current_mode != updated_mode:
            current_mode = updated_mode
            GPIO.output(output_pin, Mode_To_GPIO_Signal[current_mode])

        time.sleep(1)    
