import cv2
import Detection as detect
import Connection2 as cn
from threading import Thread
import time

speed = "50"
key = None

pipeline3, pipeline2, pipeline1 = cn.getConnection()

recvSign = Thread(target = cn.recvVarFrame, args = (pipeline1, True))
#Always look for a speed sign being sent from the raspberry pi
recvSign.start()
#cn.setConnection()

while True:
    frame = cn.recvVarFrame(pipeline3, False)

    cv2.imshow("frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        cn.sendData("FL", pipeline2)
        break
    elif key == ord('e'):
        cn.sendData("SS", pipeline2)
        break

cv2.destroyAllWindows()
cn.close()
