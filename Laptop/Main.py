import cv2
import Detection as detect
import Connection2 as cn
from threading import Thread

speed = "50"
key = None

pipeline3, pipeline2, pipeline1 = cn.getConnection()

recvSign = Thread(target = cn.recvSign, args = (pipeline1,))
#Always look for a speed sign being sent from the raspberry pi
recvSign.start()
#cn.setConnection()
while True:
    size, reso = cn.recvDimensions(pipeline3)
    if size != None:
        data = cn.recvall(size, pipeline3)
        if data != None or '':
            frame = cn.reform(data, 3, 640, 480)
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
