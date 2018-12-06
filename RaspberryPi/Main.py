from threading import Thread
import Connection as cn
import Camera as cam
import time
import DistanceSensor as dist
import DriveCar as dc
<<<<<<< HEAD
c, r = cn.getConnection()
=======
import Direction as dr
c, r = cn.setConnection()
speed = 0.2
direction = "3"
>>>>>>> 8686e577f82a676ce434c031623075ad2c17f0e7
"""time.sleep(1)
r = cn.getConnection()"""
recvSpeed = Thread(target = cn.recvData)
recvSpeed.start()
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
    speed = getSpeed()
    direction = dr.getDirection(averageX)
    dc.setVariables(direction, speed)
    
    
