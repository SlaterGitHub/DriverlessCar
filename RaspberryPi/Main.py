from threading import Thread
import Connection as cn
import Camera as cam
import time
import sys
import cv2
#import DistanceSensor as dist
#import DriveCar as dc
import Detection as detect
import Direction as dr

startProgram = time.time()
speed = 50
direction = 3
distance = 50
c = cn.getConnection()
"""time.sleep(1)
r = cn.getConnection()"""
#recvSpeed = Thread(target = cn.recvData)
#recvSpeed.start()
#Thread(target = dist.findDistance)

#Drive = Thread(target = dc.setDirection)
#Drive.start()

def finish(finalFrame, finalDistance, finalSpeed, programDuration, failure):
    data = [finalDistance, finalSpeed, programDuration, failure]
    cn.sendFinals(finalFrame, data)

while True:
    frame = cam.getFrame()
    cv2.waitKey(1)
    stopSigns, speedSigns, grey = detect.setCascFilter(frame)
    frame, averageX = detect.getPath(frame, grey)
    frame = detect.getSign(frame, speedSigns)
    frame = detect.getSign(frame, stopSigns)
    for (x, y, w, h) in speedSigns:
        Thread(target = cn.sendData, args = (grey[y:y+h, x:x+w], c)).start()

    if averageX != None:
        direction = dr.getDirection(averageX)
        cv2.circle(frame, (averageX, 205), 3, (0, 255, 255), -1)

    cv2.rectangle(frame, (0, 200), (320, 210), (0,255,0), 3)
    recievedSpeed = cn.getSpeed()
    if recievedSpeed == 'FL':
        finish(frame, distance, speed, (time.time()-startProgram), "1")
        #dc.setSpeed(0)
        #dc.setDirection(3)
        break
    elif recievedSpeed == 'SS':
        finish(frame, distance, speed, (time.time()-startProgram), "0")
        break
    elif recievedSpeed != speed:
        if recievedSpeed != None:
            speed = recievedSpeed
            #dc.setSpeed(speed)

    #distance = dist.getDistance()

    """if distance < 10:
        speed = 0
        """
    for (x, y, w, h) in  stopSigns:
        speed = 0

    #dc.setDirection(direction)

    if frame is not None:
        cn.sendFrame(frame)


time.sleep(2)
cn.endConnection()
sys.exit()
