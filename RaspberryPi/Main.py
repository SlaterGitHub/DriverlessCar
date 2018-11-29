from threading import Thread
import Connection as cn
import Camera as cam
import time
#import DistanceSensor as dist
import DriveCar as dc
c, r = cn.setConnection()

direction = 3
speed = 0.2

"""time.sleep(1)
r = cn.getConnection()"""
drive = Thread(target = dc.setDirection)

drive.start()

while True:
    frame = cam.getFrame()
    w, h = frame.shape[:2]
    #print(str(w), "x", str(h))
    cn.sendData(frame, c)
    direction, speed = cn.recvData()
    print("-----------------------------------------------------")
    print(direction)
    print(speed)
    print("_________________________________________________________")
    dc.setVariables(direction, speed)
    #distance = dist.getDistance()

drive.join()
