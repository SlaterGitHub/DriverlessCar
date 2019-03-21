import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
"""import libraries"""

sender = 12
reciever = 16
"""Set the pin that that sending speaker and recvieving mic are wired to"""

GPIO.setup(sender,GPIO.OUT)
GPIO.setup(reciever,GPIO.IN)
"""The the board what type of pin the pins are"""

def findDistance():
    distance = 0
    global distance
    while(True):
        GPIO.output(sender, False)
        time.sleep(0.0001)
        """Make sure the speaker is off"""

        GPIO.output(sender, True)
        time.sleep(0.00001)
        GPIO.output(sender, False)
        """turn the speaker on for 0.1 milliseconds as sound moves very fast"""

        while GPIO.input(reciever)==0:
          pulse_start = time.time()
        """Keep setting the time to the current time until a pulse is recieved"""

        while GPIO.input(reciever)==1:
          pulse_end = time.time()
        """When a pluse is recieved set the end time to current time"""

        pulse_duration = pulse_end - pulse_start
        """find the time between pulses"""

        dis = pulse_duration * 17150
        """find the distance in cm to the object"""

        distance = round(dis, 2)
        """round the distance to 2 decimal points"""


def getDistance():
    global distance
    return distance
    """Give the most recent distance to whoever calls this method"""
