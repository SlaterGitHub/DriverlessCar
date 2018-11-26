import RPi.GPIO as gpio
gpio.setmode(gpio.BOARD)
gpio.setup(7, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(13, gpio.OUT)
gpio.setup(15, gpio.OUT)

def forward(speed):
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(speed)
    stop()

def stop():
    gpio.output(7, False)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, False)

def setDirection(direction, speed):
    if path == '0':
        forward(speed)
    elif path == '1':
        left(speed)
    elif path == '2':
        right(speed)
    elif path == '3':
        stop(speed)

    #Code right and left
