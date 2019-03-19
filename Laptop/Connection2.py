import socket
import numpy as np
import lz4.frame
import Detection as dt
import time
"""import libraries"""

socketNum = 5001
ip = "localhost"
pipeline1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pipeline2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pipeline3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""define the ip and socket number of the host and three pipelines"""

size = None
resolution = None
text = None
"Define variables"

def getConnection():
    #Recieve connection with client
    pipeline1.connect((ip, socketNum))
    pipeline2.connect((ip, socketNum + 100))
    pipeline3.connect((ip, socketNum + 200))
    """connect to client with different sockets for each pipeline"""
    pipeline1.settimeout(0.4)
    pipeline2.settimeout(0.4)
    pipeline3.settimeout(5)
    """set a timeout for the pipelines as to cancel any data that is not
    recieved in a time period, this stops the program hanging"""

    print("Pipeline --> Raspberry: Connected")
    return pipeline3, pipeline2, pipeline1

def close():
    pipeline1.setblocking(0)
    pipeline2.setblocking(0)
    pipeline3.setblocking(0)
    pipeline1.close()
    pipeline2.close()
    pipeline3.close()
    """Ends connection with server"""

def recvall(dataSize, pipeline):
    data = b''
    """Make empty byte variable"""

    while len(data) < dataSize:
        try:
            packet = pipeline.recv(dataSize - len(data))
        except:
            return None
        if not packet:
            return None
        data += packet
    return data
    """while the varibale 'data' is not as long as the frame being recieved,
    keep getting more data from the pipeline, reducing the data being asked to
    make sure not too much is being asked for. Once 'data' is as large as the
    data expected, return the packet."""

def recvVarFrame(pipeline, speedSign):
    global text
    try:
        size = pipeline.recv(6)
        resolution = pipeline.recv(3)
    except:
        size = None
        resolution = None
    """Try to get the size and resolution of the frame and if the pipeline has
    no data set both variables to None"""

    if (size != None or '') and (resolution != None or ''):
        size = splitData(size)
        resolution = splitData(resolution)
        data = recvall(size, pipeline)
        """If data is found in the pipeline then send it through the split data
        functions and recieve the frame of the size found"""

        if data != None or '':
            if speedSign == True:
                frame = reform(data, 1, resolution, resolution)
                recvText = dt.getText(frame)
                if recvText != text or None:
                    text = recvText
                    sendData(text)
            else:
                frame = reform(data, 3, 320, 240)
                return frame
            """Make sure that a frame is found and if it is check if the frame
            is of a speed sign or a full frame. If the frame is a speed sign
            then reform the frame as a 1 channel grey scale image. If the frame
            is a full frame reform it as a 3 channel colour image"""

    return None

def reform(data, channels, x, y):
    try:
        data = lz4.frame.decompress(data)
        data = np.fromstring(data, dtype = "uint8")
        frame = data.reshape((y, x, channels))
        return frame
    except:
        return None
    """When reforming the frame, decompress the data and convert it to a 8 bit
    integer, finally take the pixels from a 1d array and make them a 2d array
    using reshape"""

def sendData(text):
    data = str(text)
    pipeline2.sendall(data)
    """Convert the text to a string and send it down pipeline2"""

def recvFinals():
    frame = None
    recieved = False
    while (recieved == False):
        if frame is None:
            frame = recvVarFrame(pipeline3, False)
            datas = recvall(9, pipeline3)
            if (frame is not None) and (datas != None or ''):
                recieved = True
    """Keep checking for the last frame and data before closing the drive"""
    
    finalDistance = splitData(datas[:3])
    finalSpeed = splitData(datas[3:5])
    progDuration = splitData(datas[5:8])
    fail = datas[8]
    return frame, finalDistance, finalSpeed, progDuration, fail
    """Split the data found into distance, speed, time, fail and the frame"""

def splitData(data):
    list = (data.decode()).split(',')
    data = int(list[len(list)-1])
    return data
    """Seperate the data by CSV which wil produce a list of empty indexes except
    for the last index which will have the data needed"""

def recvTextFrame():
    while True:
        recvVarFrame(pipeline1, True)
    """Keep recieving a frame from pipeline1 until the program closes or the pipeline timeouts"""

def deform(frame):
    frame = frame.flatten()
    frame = frame.tostring()
    frame = lz4.frame.compress(frame)
    return frame
    """Make the pixels in the frame into a flat array and then convert the 8 bit
    integers into a string, finally compress the string to reduce file size"""

def recvStats(pipe):
    try:
        speed = pipe.recv(3)
        distance = pipe.recv(3)
    except:
        return None, None
    if speed is not None:
        speed = splitData(speed)
        distance = splitData(distance)
        return speed, distance
    else:
        return None, None
    """Try to recieve speed and distance from pipe and pass the data through
    splitData to make it useable"""
