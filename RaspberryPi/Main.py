from threading import Thread
import Connection as cn
import Camera as cam
import time
import sys
import cv2
#import DistanceSensor as dist
import DriveCar as dc
import Detection as detect
import Direction as dr


#x = 0
startProgram = time.time()
speed = 50
oldSpeed= speed
direction = 3
c = cn.getConnection()
"""time.sleep(1)
r = cn.getConnection()"""
#recvSpeed = Thread(target = cn.recvData)
#recvSpeed.start()
#distThread = Thread(target = dist.findDistance)
#distThread.start()

Drive = Thread(target = dc.setMovement)
Drive.start()

frame = None
sendfrm = Thread()
distance = 47

def finish(finalFrame, finalDistance, finalSpeed, programDuration, failure):
    data = [finalDistance, finalSpeed, programDuration, failure]
    cn.sendFinals(finalFrame, data)

def sendFrame(frame):
    cn.sendFrame(frame)
    return

#sndfrm = Thread(target = sendFrame, args = (frame))
#sndfrm.start()
start = time.time()
while True:

    frame = cam.getFrame()

    #cv2.waitKey(1)
    stopSigns, speedSigns, grey = detect.setCascFilter(frame)
    frame, averageX = detect.getPath(frame, grey)
    frame = detect.getSign(frame, speedSigns)
    frame = detect.getSign(frame, stopSigns)
    for (x, y, w, h) in speedSigns:
        Thread(target = cn.sendData, args = (grey[y:y+h, x:x+w], c)).start()

    if averageX != None:
        direction = dr.getDirection(averageX)
        cv2.circle(frame, (averageX, 205), 3, (0, 255, 255), -1)
    else:
        direction = dr.getDirection(averageX)

    cv2.rectangle(frame, (0, 200), (320, 210), (0,255,0), 3)
    recievedSpeed = cn.getSpeed()

    if recievedSpeed == 'FL':
        print("q pressed")
        finish(frame, int(distance), speed, (time.time()-startProgram), "1")
        dc.setDirection(4)
        break
    elif recievedSpeed == 'SS':
        print("e pressed")
        finish(frame, int(distance), speed, (time.time()-startProgram), "0")
        dc.setDirection(4)
        break
    elif  recievedSpeed is not None :
        if (recievedSpeed != speed) and (int(recievedSpeed) < 101) and (recievedSpeed != (speed/10)):
            speed = recievedSpeed

    #distance = dist.getDistance()

    """if distance < 10:
        speed = 0"""

    for (x, y, w, h) in  stopSigns:
        oldSpeed = speed
        speed = 0

    dc.setDirection(direction)
    dc.setSpeed(speed)

    #speed = oldSpeed

    if frame is not None:
        if not sendfrm.isAlive():
            sendfrm = Thread(target = sendFrame, args = (frame,))
            sendfrm.start()

    """print("------------------------------------")
    print(speed)
    print("------------------------------------")
    print(direction)"""
    start = time.time()




#sendfrm.join()
#recvSpeed.join()
#distThread.join()

#cn.endConnection()
sys.exit()
