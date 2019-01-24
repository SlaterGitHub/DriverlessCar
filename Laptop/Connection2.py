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
    pipeline2.connect((ip, socketNum + 100))
    pipeline3.connect((ip, socketNum + 200))
    #save socket as m once accepted by client
    pipeline1.settimeout(0.1)
    pipeline2.settimeout(0.1)
    pipeline3.settimeout(0.1)
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

def recvSign(pipeline):
    size, resolution = recvDimensions(pipeline)
    if (size != None or '') and (resolution != None or ''):
        list = (size.decode()).split(',')
        size = int(list[len(list)-1])
        list = (resolution.decode()).split(',')
        resolution = int(list[len(list)-1])
        data = recvall(size, pipeline1)
        #If data is found then run the recvieve all function
        if data != None or '':
            frame = reform(data, 1, reso, reso)
            frame = cv2.cvtColor(frame, GRAY2BGR)
            sendData(dt.getText(frame))
        #Convert bytes to pixels and convert then from a 1D array to a 2D array

def recvDimensions(pipeline):
        try:
            size = pipeline.recv(6)
            resolution = pipeline.recv(3)
            return size, resolution
        except:
            return None, None

def reform(data, channels, x, y):
    data = lz4.frame.decompress(data)
    data = np.fromstring(data, dtype = "uint8")
    frame = data.reshape((x, y, channels))
    return frame

def sendData(text):
    data = str(text)
    pipeline2.sendall(data)
