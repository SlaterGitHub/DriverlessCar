import socket
import numpy
import lz4.frame
socketNum = 5001
socketNum2 = 6001
ip = "localhost"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
speed = 50

def getConnection():
    s.bind(("localhost", (socketNum)))
    #Create a server side socket
    print("binded")
    s.listen(10)
    #Wait for a recieving side to connect
    speedFrame, addr = s.accept()
    #set socket to c when recieving side connects

    r.bind(("localhost", socketNum2))
    r.listen(10)
    speedtext, addr = r.accept()

    c.bind(("localhost", socketNum2))
    c.listen(10)
    fullFrame, addr = c.accept()

    #Connect to server side of socket
    return speedFrame, speedText

def getSpeed():
    data = speedText.recv(2)
    if data != None or '':
        speed = int(data.decode())
        return speed
    return speed

def sendData(frame, c):
    reso = frame.shape[1]
    datas = prepData(frame)
    size = str(len(datas))
    for x in range(6-len(size)):
        size = "," + size
    for x in range(3-len(reso)):
        reso = "," + reso
    speedFrame.sendall(size+reso+datas)
    return
    #Convert to a string form and send the entire frame

def prepData(frame):
    frame = frame.flatten()
    #Convert frame from a 2D array to a 1D array
    datas = frame.tostring()
    return lz4.frame.compress(datas)

def sendFrame(frame):
    datas = prepData(frame)
    fullFrame.sendall(datas)
