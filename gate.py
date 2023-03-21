import time, json
import RPi.GPIO as GPIO 

def gate_control_function(MQTTClient, gate_config_list):
    
    def blinkled(pin):
        GPIO.setup(pin, GPIO.OUT)
        for i in range(2):
            GPIO.output(pin, GPIO.HIGH)  # Turn on
            time.sleep(0.5)  # Sleep for 1 second
            GPIO.output(pin, GPIO.LOW)  # Turn off
            time.sleep(0.5)  # Sleep for 1 second
    
    def open_gate(client, userdata, message):
        payload = json.loads(message.payload)
        print("Opening -", payload.get("type"))
        # gate_id = payload.get("gate_id")
        # gate_config = gate_config_list[gate_id]

        # GPIO.output(gate_config['red_led_pin'], GPIO.LOW)
        # blinkled(gate_config['green_led_pin'])
        
        # GPIO.setup(gate_config['servo_pin'], GPIO.OUT)
        # servo = GPIO.PWM(gate_config['servo_pin'], 50)
        # servo.start(0)

        # def setAngle(angle):
        #     duty = angle / 18 + 2
        #     GPIO.output(gate_config['servo_pin'], True)
        #     servo.ChangeDutyCycle(duty)
        #     time.sleep(1)
        #     GPIO.output(gate_config['servo_pin'], False)
        #     servo.ChangeDutyCycle(0)
        
        # setAngle(90)
        # time.sleep(10) # Close after 10 seconds
        # blinkled(gate_config['red_led_pin'])
        # setAngle(0)
        # GPIO.output(gate_config['red_led_pin'], GPIO.HIGH)
        
        # servo.stop()
        #GPIO.cleanup()
    

    print("Subscribing to topic 'GATE_CONTROL' ...")
    MQTTClient.subscribe(topic="GATE_CONTROL", QoS=0, callback=open_gate)
