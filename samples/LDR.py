import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep # Import the sleep function from the time module
#GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

        
def ldr():
    GPIO.setup(40, GPIO.OUT)
    pin = 11
    # max_ = 0
    # min_ = float('inf')
    
    def rc_time(pin):
        count = 0
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, GPIO.LOW)
        sleep(0.1)

        GPIO.setup(pin, GPIO.IN)
        
        while (GPIO.input(pin) == GPIO.LOW):
            count += 1
        return count
    
    try:
        while True:
            count = rc_time(pin)
            print("Sensor Output:", count)
            if count > 79999:
                GPIO.output(40, GPIO.LOW)
            else:
                GPIO.output(40, GPIO.HIGH)
    except KeyboardInterrupt:
        pass
    finally:
        #print('Min: ', min_)
        #print('Max: ', max_)
        GPIO.cleanup()
        
ldr()