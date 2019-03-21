import cv2
import time
"""define variables"""

video = cv2.VideoCapture(0)
#Use opencv to recognise the USB camera
video.set(3, 320)
video.set(4, 240)
#set the resolution of the camera
#wait for camera to warm up
"""find the camera on the car and set its resolution to be 320x240"""

def getFrame():
    ret, frame = video.read()
    #recv a frame from the camera
    cv2.waitKey(1)
    return frame
    """get a frame from the camera and wait one millisecond before freeing up
    the cameras content so another frame can be recieved"""
