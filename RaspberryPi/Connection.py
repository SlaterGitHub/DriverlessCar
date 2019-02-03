import socket
import numpy
import lz4.frame
import time
socketNum = 5001
ip = "192.168.0.31"
pipeline1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pipeline2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pipeline3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
speedFrame = None
speedText = None
fullFrame = None
data = None

def getConnection():
    global speedFrame, speedText, fullFrame
    pipeline1.bind((ip, (socketNum)))
    #Create a server side socket
    pipeline1.listen(10)
    print("binded")
    #Wait for a recieving side to connect
    speedFrame, addr = pipeline1.accept()
    #set socket to c when recieving side connects

    pipeline2.bind((ip, socketNum+100))
    pipeline2.listen(10)
    speedText, addr = pipeline2.accept()

    pipeline3.bind((ip, socketNum+200))
    pipeline3.listen(10)
    fullFrame, addr = pipeline3.accept()
    speedText.settimeout(0.02)
    speedFrame.settimeout(0.2)
    #fullFrame and speedFrame are output pipelines
    #speedText is an input pipeline

    #Connect to server side of socket
    return speedFrame

def getSpeed():
    try:
        data = speedText.recv(2)
    except:
        return None
    data = data.decode()
    if data != '':
        if data == 'FL' or 'SS':
            return data
        speed = int(data)
        return speed
    return None

def sendData(frame, c):
    reso = frame.shape[1]
    datas = prepData(frame)
    size = len(datas)
    size = constVarLength(6, size)
    reso = constVarLength(3, reso)
    c.sendall(size+reso+datas)
    return
    #Convert to a string form and send the entire frame

def prepData(frame):
    frame = frame.flatten()
    #Convert frame from a 2D array to a 1D array
    datas = frame.tostring()
    return lz4.frame.compress(datas)

def sendFrame(frame):
    sendData(frame, fullFrame)

def sendFinals(finalFrame, data):
    sendFrame(finalFrame)
    data[2] = int(data[2])
    data[0] = constVarLength(3, data[0])
    data[1] = constVarLength(2, data[1])
    data[2] = constVarLength(3, data[2])
    data[3] = data[3].encode()
    fullFrame.sendall(data[0] + data[1] + data[2] + data[3])
    time.sleep(1)
    endConnection()

def constVarLength(length, var):
    var = str(var)
    for x in range(length-len(var)):
        var = ',' + var
    return var.encode()

def endConnection():
    speedFrame.close()
    speedText.close()
    fullFrame.close()
