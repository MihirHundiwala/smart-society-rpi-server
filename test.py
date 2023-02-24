import time, json
import RPi.GPIO as GPIO 

from aws.connections import MQTTClient
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8, GPIO.OUT)

def open_gate():

    servo = GPIO.PWM(8, 50)
    servo.start(0)

    def setAngle(duty):
        GPIO.output(8, True)
        servo.ChangeDutyCycle(duty)
        time.sleep(1)
        GPIO.output(8, False)
        servo.ChangeDutyCycle(0)
    
    print("Opening")
    setAngle(2)
    time.sleep(5) # Close after 10 seconds
    setAngle(7)
    
    servo.stop()
    #GPIO.cleanup()

open_gate()
