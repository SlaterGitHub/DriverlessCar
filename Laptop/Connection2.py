import socket
import numpy as np
import lz4.frame
import Detection as dt
socketNum = 5001
ip = "localhost"
pipeline1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pipeline2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
pipeline3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
size = None
resolution = None

def getConnection():
    #Recieve connection with server
    pipeline1.connect((ip, socketNum))
    #input
    pipeline2.connect((ip, socketNum + 100))
    #output
    pipeline3.connect((ip, socketNum + 200))
    #input
    #save socket as m once accepted by client
    pipeline1.settimeout(0.4)
    pipeline2.settimeout(0.4)
    pipeline3.settimeout(5)
    print("Pipeline --> Raspberry: Connected")
    return pipeline3, pipeline2, pipeline1

def close():
    pipeline1.close()
    # Ends connection with server

def recvall(dataSize, pipeline):
    data = b''
    #Make empty byte variable
    while len(data) < dataSize:
        try:
            packet = pipeline.recv(dataSize - len(data))
            #Only recieve data that is as long as needed
        except:
            return None
        if not packet:
            return None
            #If data is not found then the server hasn't sent anything
        data += packet
        #add data recieved to the total data
    return data

def recvVarFrame(pipeline, speedSign):
    try:
        size = pipeline.recv(6)
        resolution = pipeline.recv(3)
    except:
        size = None
        resolution = None
    if (size != None or '') and (resolution != None or ''):
        size = splitData(size)
        resolution = splitData(resolution)
        data = recvall(size, pipeline)
        #If data is found then run the recvieve all function
        if data != None or '':
            if speedSign == True:
                frame = reform(data, 1, reso, reso)
                frame = cv2.cvtColor(frame, GRAY2BGR)
                sendData(dt.getText(frame))
            else:
                frame = reform(data, 3, 320, 240)
                return frame
    if speedSign == False:
        return None

"""def recvDimensions(pipeline):
        size = pipeline.recv(6)
        resolution = pipeline.recv(3)
        return size, resolution"""

def reform(data, channels, x, y):
    data = lz4.frame.decompress(data)
    data = np.fromstring(data, dtype = "uint8")
    frame = data.reshape((y, x, channels))
    return frame

def sendData(text):
    data = str(text)
    pipeline2.sendall(data)

def recvFinals():
    frame = None
    recieved = False
    while (recieved == False):
        if not frame:
            frame = recvVarFrame(pipeline3, False)
            datas = recvall(8, pipeline3)
            if (frame is not None) and (datas != None or ''):
                recieved = True
    print(datas)
    finalDistance = splitData(datas[:3])
    finalSpeed = splitData(datas[3:5])
    progDuration = splitData(datas[5:8])
    return frame, finalDistance, finalSpeed, progDuration

def splitData(data):
    list = (data.decode()).split(',')
    data = int(list[len(list)-1])
    return data
