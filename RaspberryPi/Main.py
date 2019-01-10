from threading import Thread
import Connection as cn
import Camera as cam
import time
import DistanceSensor as dist
import DriveCar as dc
import Detection as detect
import Direction as dr

speed = 0.02
direction = 3
#c, r = cn.getConnection()
"""time.sleep(1)
r = cn.getConnection()"""
#recvSpeed = Thread(target = cn.recvData)
#recvSpeed.start()
Thread(target = dist.findDistance)

Drive = Thread(target = dc.setDirection)
Drive.start()
while True:
    frame = cam.getFrame()
    stopSigns, speedSigns, grey = detect.setCascFilter(frame)
    frame, averageX = detect.getPath(frame, grey)
    frame = detect.getSign(frame, speedSigns)
    frame = detect.getSign(frame, stopSigns)

    for (x, y, w, h) in speedSigns:
        Thread(target = cn.sendData, args = (grey[y:y+h, x:x+w], c)).start()

    speed = cn.getSpeed()

    if averageX != None:
        direction = dr.getDirection(averageX)
        cv2.circle(frame, (averageX, 205), 3, (0, 255, 255), -1)

    cv2.rectangle(frame, (0, 200), (320, 210), (0,255,0), 3)

    distance = dist.getDistance()

    if distance < 10:
        speed = 0

    for (x, y, w, h) in  stopSigns:
        speed = 0

    dc.setVariables(direction, speed)
