import socket
import numpy
import lz4.frame
import time
"""import libraries"""

socketNum = 5001
ip = "192.168.0.28"
pipeline1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pipeline2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pipeline3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""define the ip and socket number of the host and three pipelines"""

speedFrame = None
speedText = None
fullFrame = None
data = None
"""Define pipeline variables and data to start as empty"""

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
    """for every pipeline, bind it to a socket within the target ip and listen for a connection and set them to be one of
    the pipeline variables. Set a timeout for each pipeline"""

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
    """recieve two bytes of data from speedText pipeline. decode the data and if
    is not empty then check if the data is FL or SS then return the data, if not then
    convert it to an integer and return the data"""

def sendData(frame, c):
    reso = frame.shape[1]
    datas = prepData(frame)
    size = len(datas)
    size = constVarLength(6, size)
    reso = constVarLength(3, reso)
    c.sendall(size+reso+datas)
    return
    """get the resolution of one of the axis of the frame as only one is needed.
    Then prep the frame to be in compressed string form. Get the size of
    the frame and make the size and resolution constant length so they can be recieved
    correctly. Finally combine the size, resolutoin and frame and send it to the server"""

def prepData(frame):
    frame = frame.flatten()
    #Convert frame from a 2D array to a 1D array
    datas = frame.tostring()
    return lz4.frame.compress(datas)
    """convert the frame to a 1d array then make it a string and compress the string
    to make the file smaller"""

def sendFrame(frame):
    sendData(frame, fullFrame)
    """send the full frame in the fullFrame pipeline"""

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
    """send the last frame through sendFrame. The convert all the other data
    to a constant variable length and send all the data through the repurposed
    fullFrame pipeline, finallt wait for the server to recieve it and end the
    connection with the server"""

def constVarLength(length, var):
    var = str(var)
    for x in range(length-len(var)):
        var = ',' + var
    return var.encode()
    """Convert the data to a string and find the lenght of the string. for every
    number it is not the same length, add a comma, convert the string to a bytes
    datatype and return it"""

def endConnection():
    speedFrame.close()
    speedText.close()
    fullFrame.close()
    """close all pipelines"""

def sendStats(speed, distance):
    speed = constVarLength(3, int(speed))
    distance = constVarLength(3, int(distance))
    if (speed != '') and (distance != ''):
        speedText.sendall(speed + distance)
    """set the speed and distance to be a contant length and send them through
    speedText"""
