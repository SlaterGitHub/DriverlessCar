import cv2
import Detection as detect
import Connection2 as cn
import Direction as Dir
from threading import Thread
speed = "50"
direction = "3"

recvSign = Thread(target = cn.getData)

m = cn.getConnection()

recvSign.start()
#cn.setConnection()
while True:
    """frame = cn.getData()

    stopSigns, speedSigns, grey = detect.setCascFilter(frame)
    frame, averageX = detect.getPath(frame, grey)
    frame = detect.getSign(frame, speedSigns)
    frame = detect.getSign(frame, stopSigns)
    text = detect.getText(grey, speedSigns)

    if text != None:
        if "50" in text:
            speed = "50"
            print(speed)
        elif "30" in text:
            speed = "30"
            print(speed)
        elif "20" in text:
            speed = "20"
            print(speed)
    if averageX != None:
        direction = Dir.getDirection(averageX)
    print(direction)
    cn.sendData(direction, "20", m)
    if averageX != None:
        cv2.circle(frame, (averageX, 205), 3, (0, 255, 255), -1)
    cv2.rectangle(frame, (0, 200), (320, 210), (0,255,0), 3)

    #output = cv2.resize(frame, (1280, 960), interpolation = cv2.INTER_AREA)

    try:
        cv2.imshow("output", frame)
    except:
        print("Display Error")

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break"""
cn.sendData("0", m)
cv2.destroyAllWindows()
cn.close()
