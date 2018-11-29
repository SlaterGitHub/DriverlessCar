from threading import Thread
import Connection as cn
import Camera as cam
import time
import DistanceSensor as dist
import DriveCar as dc
c, r = cn.setConnection()
"""time.sleep(1)
r = cn.getConnection()"""
direction, speed = Thread(target = cn.recvData).start()
while True:
    frame = cam.getFrame()
    cn.sendData(frame, c)
    direction, speed = cn.recvData()
    print(direction)
    print(speed)
    distance = dist.getDistance()
    dc.setDirection(direction, speed)
