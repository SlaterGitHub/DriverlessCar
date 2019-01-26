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
#set starting speed and direction to stop

wheel = [gpio.PWM(7, freq), gpio.PWM(11, freq), gpio.PWM(13, freq), gpio.PWM(15, freq)]
for x in range(4):
    wheel[x].start(0)

def forward(velocity):
    wheel[0].changeDutyCycle(velocity)
    wheel[1].changeDutyCycle(0)
    wheel[2].changeDutyCycle(0)
    wheel[3].changeDutyCycle(velocity)

def left(velocity):
    wheel[0].changeDutyCycle(velocity)
    wheel[1].changeDutyCycle(0)
    wheel[2].changeDutyCycle(velocity)
    wheel[3].changeDutyCycle(0)

def right(velocity):
    wheel[0].changeDutyCycle(0)
    wheel[1].changeDutyCycle(velocity)
    wheel[2].changeDutyCycle(0)
    wheel[3].changeDutyCycle(velocity)

def stop(velocity):
    for x in range(4):
        wheel[x].changeDutyCycle(velocity)
"""When a function runs it changes the voltage given to each motor to get the direction
needed and turns the motor off and on at a high frequancy to make the car move
different speeds"""

def accelerate(finalSpeed):
    global velocity
    changeInSpeed = finalSpeed - velocity
    timeInterval = 1/changeInSpeed
    for x in range(changeInSpeed):
        velocity -= x
        time.sleep(timeInterval)
    return

def setDirection():
    while True:
        global path
        global velocity
        print(path)
        if path == 0:
            forward(freq)
        elif path == 1:
            left(freq)
        elif path == 2:
            right(freq)
        elif path == 3:
            stop(freq)
    """Depending on the value of path, 1 of 4 functions are run and passed the speed"""

def setDirection(direction):
    global path
    path = direction

def setSpeed(speed):
    global velocity
    if (speed != (0.5 * velocity)) and (speed != None):
        velocity = 2 * speed
        Thread(target = accelerate, args = velocity).start()
