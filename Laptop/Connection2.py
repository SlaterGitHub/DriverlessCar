import socket
import numpy as np
import math
socketNum = 5001
socketNum2 = 6001
ip = "192.168.0.29"
ip2 = "192.168.0.27"
x = 0
y = 0
dataSize = 0
w = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def getConnection():
    print(ip)
    w.connect((ip, socketNum))
    print("Laptop <-- Pipeline: Connected")

    """r.bind((ip2, socketNum2))
    r.listen(10)
    m, addr = r.accept()
    print("Pipeline --> Raspberry: Connected")"""
    m = None
    return m

"""def setConnection():
    r.bind(("localhost", socketNum2))
    r.listen(10)
    m, addr = r.accept()
    print("Pipeline --> Raspberry: Connected")"""

def close():
    w.close()

def recvall(dataSize):
    data = b''
    while len(data) < dataSize:
        packet = w.recv(dataSize - len(data))
        if not packet:
            return None
        data += packet
    return data

def getData():
    data = str(w.recv(14))
    dataSize, x, y = int(data.split(","))

    if data != None or '':
        data = recvall(dataSize)
        if not data:
            return None
        frame = np.fromstring(data, dtype=np.uint8)
        return frame.reshape((y, x, 3))

def sendData(direction, text, m):
    data = str(direction) + str(text)
    m.sendall(data)
