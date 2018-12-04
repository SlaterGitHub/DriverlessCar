import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BOARD)
gpio.setup(7, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)
#create gpio and set pins to be output mode

path = 3
freq = 0.2
#set starting speed and direction to stop

def forward(speed):
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(speed)
    stop(speed)

def left(speed):
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(speed)
    stop(speed)

def right(speed):
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(speed)
    stop(speed)

def stop(speed):
    gpio.output(7, False)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, False)
    time.sleep(speed)
"""When a function runs it changes the voltage given to each motor to get the direction
needed and turns the motor off and on at a high frequancy to make the car move
different speeds"""

def setDirection():
    global path
    global freq
        while True:
            if path == 0:
                forward(freq)
            elif path == 1:
                left(freq)
            elif path == 2:
                right(freq)
            elif path == 3:
                stop(freq)
    """Depending on the value of path, 1 of 4 functions are run and passed the speed"""

def setVariables(direction, speed):
    path = direction
    freq = speed
    #Set the variables in the class
