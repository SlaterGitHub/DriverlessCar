import cv2
import Detection as detect
import Connection2 as cn
from threading import Thread
import time
import sys
import UIpanel

speed = "50"
key = None

#pipeline3, pipeline2, pipeline1 = cn.getConnection()

StartUI = [[150, 25], [43, 3], ["", "Database"], ["Text", "Button"], [[0,0], [0,1]]]

HomeUI = UIpanel.UIpanel(StartUI[0], StartUI[1], StartUI[2], StartUI[3], StartUI[4])

HomeUI.showPanel()

sys.exit()

recvSign = Thread(target = cn.recvTextFrame)
#Always look for a speed sign being sent from the raspberry pi
recvSign.start()
#cn.setConnection()

while True:
    frame = cn.recvVarFrame(pipeline3, False)
    if frame is not None:
        cv2.imshow("frame", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        cn.sendData("FL")
        break
    elif key == ord('e'):
        cn.sendData("SS")
        break

time.sleep(0.1)

finalFrame, finalDistance, finalSpeed, progDuration, fail = cn.recvFinals()
print(finalDistance)
print(finalSpeed)
print(progDuration)
print(fail)
""" UPLOAD TO DATABASE """

cv2.destroyAllWindows()
#cn.close()
#recvSign.join()
sys.exit()
