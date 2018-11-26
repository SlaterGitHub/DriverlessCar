import socket
import numpy
socketNum = 5001
socketNum2 = 6001
ip = "localhost"
dataSize = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def setConnection():
    s.bind(("localhost", (socketNum)))
    print("binded")
    s.listen(10)
    c, addr = s.accept()

    r.connect((ip, socketNum2))
    return c, r

"""def getConnection():
    r.connect((ip, socketNum2))
    return r"""

def recvData():
    while True:
        speedDirect = r.recv(3)
        if not speedDirect:
            return None, None
        direction, speed = speedDirect[:1], speedDirect[1:3]
        speed = 1.0 / float(speed)
        return direction, speed

def sendData(frame, c):
    frame = frame.flatten()
    datas = frame.tostring()
    c.sendall(datas)
