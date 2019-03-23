from threading import Thread
import Connection as cn
import Camera as cam
import time
import sys
import cv2
import DistanceSensor as dist
import DriveCar as dc
import Detection as detect
import Direction as dr
"""import libraries"""

speed = 50
direction = 3
"""define starter speed and direction"""

c = cn.getConnection()
"""connect to the server"""

startProgram = time.time()
"""get time at start of program"""

distThread = Thread(target = dist.findDistance)
distThread.start()
"""Start thread to constantly recvieve speed sign text and thread to get distance from distance sensor"""

Drive = Thread(target = dc.setMovement)
Drive.start()
"""Start thread to constantly drive the motors of the car"""

frame = None
sendfrm = Thread()
distance = 47
"""define frame as empty to begin with, sendfrm as an empty thread and distance as 47 as a placeholder until a real one is found"""

def finish(finalFrame, finalDistance, finalSpeed, programDuration, failure):
    data = [finalDistance, finalSpeed, programDuration, failure]
    cn.sendFinals(finalFrame, data)
    """Get the final data and make it a list then send the list to the connection class to send to the server"""

def sendFrame(frame):
    cn.sendFrame(frame)
    return
    """send a full frame to the server"""
while True:
    frame = cam.getFrame()
    stopSigns, speedSigns, grey = detect.setCascFilter(frame)
    frame, averageX = detect.getPath(frame, grey)
    frame = detect.getSign(frame, speedSigns)
    frame = detect.getSign(frame, stopSigns)
    """Get a frame from the camera and send it through the processing functions.
    setCascFilter will make a grey version of thr frame and find the speed and stop signs.
    getPath will find any red within a section of the frame and return the frame with greyed out
    pixels where red isn't found along with a co-ordinate of the middle of the road.
    getSign returns the co-ordinates of the location of the speed and stop sign"""
    for (x, y, w, h) in speedSigns:
        Thread(target = cn.sendData, args = (grey[y:y+h, x:x+w], c)).start()
        """if a speed sign is found then the sectio of the frame with the sign is
        sent to the server through a thread"""

    direction = dr.getDirection(averageX)

    if averageX != None:
        cv2.circle(frame, (averageX, 205), 3, (0, 255, 255), -1)
    """Use getDirection to make the location of the middle of the road find in the boundaries
    of -160 to 160.
    If a point for the middle of the road is found then draw the point on the frame."""

    cv2.rectangle(frame, (0, 200), (320, 210), (0,255,0), 3)
    recievedSpeed = cn.getSpeed()
    """draw a rectangle where the frame has been scannde for road and get a speed from
    the server"""

    if recievedSpeed == 'FL':
        finish(frame, int(distance), speed, (time.time()-startProgram), "1")
        dc.setDirection(4)
        break
    elif recievedSpeed == 'SS':
        finish(frame, int(distance), speed, (time.time()-startProgram), "0")
        dc.setDirection(4)
        break
        """if the server says the speed is FL (fail) or SS (success) then send the final data
        to finish and set the direction to 4 (stop immediatly)"""
    elif  recievedSpeed is not None :
        recievedSpeed = int(recievedSpeed)
        if (recievedSpeed != speed) and (recievedSpeed < 101) and (recievedSpeed != (speed/10)):
            speed = recievedSpeed
    """if the server returns a value, convert it to an integer. If the new speed is not the old speed,
    is less than 101 (as the speed limit will be no higher than 100mph) and the speed is not the old speed
    divided by 10, this is to catch any times the server only finds the first digit in the speed sign"""

    distance = dist.getDistance()
    """get the distance from the distance class"""

    if distance < 10:
        speed = 0
    """if the car is 10cm away from an object, stop the car"""

    for (x, y, w, h) in  stopSigns:
        speed = 0
        """If a stop sign is found, stop the car"""

    dc.setDirection(direction)
    dc.setSpeed(speed)
    cn.sendStats(speed, distance)
    """Set the direction and speed of the cars motors. Send the speed and distance
    recorded by the car to the server"""

    if frame is not None:
        if not sendfrm.isAlive():
            sendfrm = Thread(target = sendFrame, args = (frame,))
            sendfrm.start()
    """If a frame is found and isn't already being sent then set sendfrm to send
    the new frame"""

sys.exit()
"""end the program"""
