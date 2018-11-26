from threading import Thread
import Connection as cn
import Camera as cam
import time
#import DistanceSensor as dist
#import DriveCar as d
c, r = cn.setConnection()
"""time.sleep(1)
r = cn.getConnection()"""
#direction, speed = Thread(target = cn.recvData).start()
while True:
    frame = cam.getFrame()
    #w, h = frame.shape[:2]
    #print(str(w), "x", str(h))
    cn.sendData(frame, c)
    direction, speed = cn.recvData()
    print(direction)
    print(speed)
    #distance = dist.getDistance()
    #dc.setDirection(direction, speed)
