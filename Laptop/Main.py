import cv2
import Detection as detect
import Connection2 as cn
from threading import Thread

speed = "50"

recvSign = Thread(target = cn.recvSign)
#Always look for a speed sign being sent from the raspberry pi

pipeline3, pipeline2 = cn.getConnection()

recvSign.start()
#cn.setConnection()
while True:
    data = recvall(921600, pipeline3)

    if data != None or '':
        frame = reform(data, 3, 640, 480)

    cv2.imshow(frame, "Car View")

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        cn.sendData("FL", pipeline2)
        break
    elif key == ord('e'):
        cn.sendData("FL", pipeline2)
        break

cv2.destroyAllWindows()
cn.close()
