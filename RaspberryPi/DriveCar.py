import RPi.GPIO as gpio
import time
from threading import Thread
gpio.setmode(gpio.BOARD)
gpio.setup(7, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)
#create gpio and set pins to be output mode

path = 3
freq = 50
velocity = 50
currVelocity = velocity
#set starting speed and direction to stop

wheel = [gpio.PWM(7, freq), gpio.PWM(11, freq), gpio.PWM(13, freq), gpio.PWM(15, freq)]
for x in range(4):
    wheel[x].start(0)

def forward(velocity):
    wheel[0].ChangeDutyCycle(currVelocity)
    wheel[1].ChangeDutyCycle(0)
    wheel[2].ChangeDutyCycle(0)
    wheel[3].ChangeDutyCycle(currVelocity)

def left(velocity):
    wheel[0].ChangeDutyCycle(currVelocity)
    wheel[1].ChangeDutyCycle(0)
    wheel[2].ChangeDutyCycle(currVelocity)
    wheel[3].ChangeDutyCycle(0)

def right(velocity):
    wheel[0].ChangeDutyCycle(0)
    wheel[1].ChangeDutyCycle(currVelocity)
    wheel[2].ChangeDutyCycle(0)
    wheel[3].ChangeDutyCycle(currVelocity)

def stop(velocity):
    for x in range(4):
        wheel[x].ChangeDutyCycle(currVelocity)
"""When a function runs it changes the voltage given to each motor to get the direction
needed and turns the motor off and on at a high frequancy to make the car move
different speeds"""

def accelerate(finalSpeed):
    global velocity, currVelocity
    changeInSpeed = finalSpeed - currVelocity
    timeInterval = 1/changeInSpeed
    for x in range(changeInSpeed):
        currVelocity += x
        time.sleep(timeInterval)
    return

def setMovement():
    while True:
        global path
        global currVelocity
        print(currVelocity)
        if path == 0:
            forward(currVelocity)
        elif path == 1:
            left(currVelocity)
        elif path == 2:
            right(currVelocity)
        elif path == 3:
            stop(currVelocity)
    """Depending on the value of path, 1 of 4 functions are run and passed the speed"""

def setDirection(direction):
    global path
    path = direction

def setSpeed(speed):
    global velocity
    if (speed != None):
        speed = int(speed)
        if (speed != velocity / 2):
            velocity = 2 * speed
            Thread(target = accelerate, args = [velocity]).start()
