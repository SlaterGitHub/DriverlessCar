import cv2
import numpy
import time

vid = cv2.VideoCapture(0)
vid.set(3, 640)
vid.set(4, 480)

time.sleep(0.1)

def getFrame():
    while True:
        ret, frame = vid.read()
        return frame
