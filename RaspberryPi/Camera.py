import cv2
import time

video = cv2.VideoCapture(0)
#Use opencv to recognise the USB camera
video.set(3, 640)
video.set(4, 480)
#set the resolution of the camera
#wait for camera to warm up

def getFrame():
    ret, frame = video.read()
    cv2.imshow("test", frame)
    #recv a frame from the camera
    cv2.waitKey(1)
    return frame
