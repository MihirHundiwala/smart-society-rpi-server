import time
import RPi.GPIO as GPIO 

def gate_control_function(MQTTClient):
    #gate_control_function.stop = False # Function attribute used for stopping thread
    
    def blinkled(pin):
        GPIO.setup(pin, GPIO.OUT)
        for i in range(2):
            GPIO.output(pin, GPIO.HIGH)  # Turn on
            time.sleep(0.5)  # Sleep for 1 second
            GPIO.output(pin, GPIO.LOW)  # Turn off
            time.sleep(0.5)  # Sleep for 1 second
    
    def open_gate(client, userdata, message):
        
        GPIO.output(12, GPIO.LOW)
        blinkled(10)
        
        GPIO.setup(8, GPIO.OUT)
        servo = GPIO.PWM(8, 50)
        servo.start(0)

        def setAngle(angle):
            duty = angle / 18 + 2
            GPIO.output(8, True)
            servo.ChangeDutyCycle(duty)
            time.sleep(1)
            GPIO.output(8, False)
            servo.ChangeDutyCycle(0)
        
        print("Opening")
        setAngle(90)
        time.sleep(3) # Close after 3 seconds
        blinkled(12)
        setAngle(0)
        GPIO.output(12, GPIO.HIGH)
        
        servo.stop()
        #GPIO.cleanup()
    

    print("Subscribing to topic 'GATE_CONTROL' ...")
    MQTTClient.subscribe(topic="GATE_CONTROL", QoS=0, callback=open_gate)
