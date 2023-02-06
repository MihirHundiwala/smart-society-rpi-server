import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)  
GPIO.setup(8,GPIO.IN)
GPIO.setup(10,GPIO.OUT)     
while True:  
    if (GPIO.input(8)):
        print("Water Inadequate")
        GPIO.output(10,GPIO.HIGH)
    else:
        print("Water Adequate")
        GPIO.output(10,GPIO.LOW)
    time.sleep(2)