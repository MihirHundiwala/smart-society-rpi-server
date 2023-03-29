# import time, json
# import RPi.GPIO as GPIO 

# from aws.connections import MQTTClient
# GPIO.setmode(GPIO.BOARD)
# GPIO.setup(8, GPIO.OUT)

# def open_gate():

#     servo = GPIO.PWM(8, 50)
#     servo.start(0)

#     def setAngle(duty):
#         GPIO.output(8, True)
#         servo.ChangeDutyCycle(duty)
#         time.sleep(1)
#         GPIO.output(8, False)
#         servo.ChangeDutyCycle(0)
    
#     print("Opening")
#     setAngle(2)
#     time.sleep(5) # Close after 10 seconds
#     setAngle(7)
    
#     servo.stop()
#     #GPIO.cleanup()

# open_gate()


# import serial
# import adafruit_fingerprint

# uart = serial.Serial("/dev/ttyS0", baudrate=57600, timeout=1)
# finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

# finger.empty_library()
# finger.read_templates()

# print(finger.templates)

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
print("Setting up Raspberry PI...")

value = GPIO.LOW
GPIO.setup(11, GPIO.OUT)
GPIO.output(11, value)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, value)
GPIO.setup(15, GPIO.OUT)
GPIO.output(15, value)

while True:
    pass

# GPIO.cleanup()
