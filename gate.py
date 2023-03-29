import time, json
import RPi.GPIO as GPIO 
from config import gate_config_list
from aws.functions import iot_publish

def blinkled(pin):
    GPIO.setup(pin, GPIO.OUT)
    for i in range(2):
        GPIO.output(pin, GPIO.HIGH)  # Turn on
        time.sleep(0.5)  # Sleep for 1 second
        GPIO.output(pin, GPIO.LOW)  # Turn off
        time.sleep(0.5)  # Sleep for 1 second


def open_gate(gate_id, MQTTClient, payload, topic):
        print("Opening gate")
        gate_config = gate_config_list[gate_id]

        GPIO.setup(gate_config['red_led_pin'], GPIO.OUT)
        GPIO.setup(gate_config['green_led_pin'], GPIO.OUT)

        GPIO.output(gate_config['red_led_pin'], GPIO.LOW)
        blinkled(gate_config['green_led_pin'])
        
        GPIO.setup(gate_config['servo_pin'], GPIO.OUT)
        servo = GPIO.PWM(gate_config['servo_pin'], 50)
        servo.start(0)

        def setAngle(angle):
            duty = angle / 18 + 2
            GPIO.output(gate_config['servo_pin'], True)
            servo.ChangeDutyCycle(duty)
            time.sleep(1)
            GPIO.output(gate_config['servo_pin'], False)
            servo.ChangeDutyCycle(0)
        
        setAngle(gate_config["angle1"])
        iot_publish(MQTTClient, topic = topic, payload = payload)
        time.sleep(5) # Close after 10 seconds
        blinkled(gate_config['red_led_pin'])
        setAngle(gate_config["angle2"])
        GPIO.output(gate_config['red_led_pin'], GPIO.HIGH)
        
        servo.stop()


def gate_control_function(MQTTClient, gate_config_list):

    for gate_config in gate_config_list:
        GPIO.output(gate_config['red_led_pin'], GPIO.HIGH)

    
    def open_gate_on_publish(client, userdata, message):
        print("Opening gate")
        payload = json.loads(message.payload)
        gate_id = int(payload.get("gate_id"))
        gate_config = gate_config_list[gate_id]

        GPIO.setup(gate_config['red_led_pin'], GPIO.OUT)
        GPIO.setup(gate_config['green_led_pin'], GPIO.OUT)

        blinkled(gate_config['green_led_pin'])
        
        GPIO.setup(gate_config['servo_pin'], GPIO.OUT)
        servo = GPIO.PWM(gate_config['servo_pin'], 50)
        servo.start(0)

        def setAngle(angle):
            duty = angle / 18 + 2
            GPIO.output(gate_config['servo_pin'], True)
            servo.ChangeDutyCycle(duty)
            time.sleep(1)
            GPIO.output(gate_config['servo_pin'], False)
            servo.ChangeDutyCycle(0)
        
        setAngle(gate_config["angle1"])
        time.sleep(5) # Close after 5 seconds
        blinkled(gate_config['red_led_pin'])
        setAngle(gate_config["angle2"])
        GPIO.output(gate_config['red_led_pin'], GPIO.HIGH)
        
        servo.stop()
    

    print("Subscribing to topic 'GATE_CONTROL' ...")
    MQTTClient.subscribe(topic="GATE_CONTROL", QoS=1, callback=open_gate_on_publish)
