import RPi.GPIO as GPIO
import time.sleep

GPIO.setmode(GPIO.BCM)
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
    
def getDistance():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    sent = time.time()
    recv = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        sent = time.time()
    while GPIO.input(GPIO.ECHO) == 1:
        EchoTime = recv - sent
        distance = (EchoTime * 34300) / 2
        distance = distance / 0.000058
        gpio.cleanup()
        return distance
