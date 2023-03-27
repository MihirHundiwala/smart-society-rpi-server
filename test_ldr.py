import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

def rc_time ():
    count = 0
  
    #Output on the pin for 
    GPIO.setup(8, GPIO.OUT)
    GPIO.output(8, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(8, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(8) == GPIO.LOW):
        count += 1

    return count

#Catch when script is interrupted, cleanup correctly
try:
    # Main loop
    while True:
        print(rc_time())
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()