import cv2
import numpy
import time

vid = cv2.VideoCapture(0)
#Use opencv to recognise the USB camera
vid.set(3, 640)
vid.set(4, 480)
#set the resolution of the camera

time.sleep(0.3)
#wait for camera to warm up

def getFrame():
    ret, frame = vid.read()
    #recv a frame from the camera
    return frame
