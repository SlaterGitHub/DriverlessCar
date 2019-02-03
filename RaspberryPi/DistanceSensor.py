import RPi.GPIO as GPIO
import time
#import libraries

GPIO.setmode(GPIO.BOARD)
#set GPIO to be pin names
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
#set pin 18 to be an output pin
GPIO.setup(GPIO_ECHO, GPIO.IN)
#set pin 24 to be an input pin

distance = 50

def findDistance():
    GPIO.output(GPIO_TRIGGER, True)
    #output voltage
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    #stop outputing voltage
    sent = time.time()
    recv = time.time()
    #Get curent time

    while GPIO.input(GPIO_ECHO) == 0:
        sent = time.time()
        #update time sent while pin 18 doesn't detect voltage
    while GPIO.input(GPIO.ECHO) == 1:
        EchoTime = recv - sent
        #Calculate time between sent and recieved
        distance = (EchoTime * 34300) / 2
        #get distance to object and back,
        #then divide it by 2 to get distance to object
        distance = distance / 0.000058
        #Convert distance to cm measurement
        gpio.cleanup()
        #set pins back to default settings

def getDistance():
    global distance
    return distance
