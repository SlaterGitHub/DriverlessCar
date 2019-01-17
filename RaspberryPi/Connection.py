import socket
import numpy
import lz4.frame
socketNum = 5001
ip = "localhost"
pipeline1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pipeline2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pipeline3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
speed = 50

def getConnection():
    pipeline1.bind(("localhost", (socketNum)))
    #Create a server side socket
    print("binded")
    pipeline1.listen(10)
    #Wait for a recieving side to connect
    speedFrame, addr = pipeline1.accept()
    #set socket to c when recieving side connects

    pipeline2.bind(("localhost", socketNum+100))
    pipeline2.listen(10)
    speedtext, addr = pipeline2.accept()

    pipeline3.bind(("localhost", socketNum+200))
    pipeline3.listen(10)
    fullFrame, addr = pipeline3.accept()

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
    c.sendall(size+reso+datas)
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
