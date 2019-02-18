import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

sender = 12 
reciever = 16

GPIO.setup(sender,GPIO.OUT)
GPIO.setup(reciever,GPIO.IN)

def findDistance():
    distance = 0
    global distance
    while(True):
        GPIO.output(sender, False)
        time.sleep(0.0001)

        GPIO.output(sender, True)
        time.sleep(0.00001)
        GPIO.output(sender, False)

        while GPIO.input(reciever)==0:
          pulse_start = time.time()

        while GPIO.input(reciever)==1:
          pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        dis = pulse_duration * 17150

        distance = round(dis, 2)


def getDistance():
    global distance
    return distance
