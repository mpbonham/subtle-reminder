import RPi.GPIO as GPIO
import time

pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(pin,GPIO.OUT)


def turn_led_pi(state):
    if state == "on":
        GPIO.output(pin,GPIO.HIGH)
    elif state == "off":
        GPIO.output(pin,GPIO.LOW)
    else:
        return "INCORRECT PARAMETER"

def breathe(seconds):
  
    GPIO.output(pin,GPIO.LOW)

    pwm = GPIO.PWM(pin,1000)
    pwm.start(0)

    # breath led for x seconds
    time_stop = time.time()+seconds
    while time.time() < time_stop:
        for x in range(0,101,5):
            pwm.ChangeDutyCycle(x)
            time.sleep(0.05)
        time.sleep(1)
        for x in range(100,-1,-5):
            pwm.ChangeDutyCycle(x)
            time.sleep(.05)
        time.sleep(1)
    pwm.stop()
    GPIO.output(pin,GPIO.LOW)

def blink(num_of_blinks):
    for x in range(num_of_blinks):
        turn_led_pi("on")
        time.sleep(.5)
        turn_led_pi("off")
        time.sleep(.5)



        
