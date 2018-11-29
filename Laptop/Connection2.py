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
    w.connect((ip, socketNum)
    #Recieve connection with server
    print("Laptop <-- Pipeline: Connected")

    r.bind((ip2, socketNum2))
    #Create a server side pipeline
    r.listen(10)
    #wait for a response
    m, addr = r.accept()
    #save socket as m once accepted by client
    print("Pipeline --> Raspberry: Connected")
    return m

def close():
    w.close()
    # Ends connection with server

def recvall(dataSize):
    data = b''
    #Make empty byte variable
    while len(data) < dataSize:
        packet = w.recv(dataSize - len(data))
        #Only recieve data that is as long as needed
        if not packet:
            return None
            #If data is not found then the server hasn't sent anything
        data += packet
        #add data recieved to the total data
    return data

def getData():
    data = str(w.recv(14))
    #Only listen for data that is 14 bytes long
    dataSize, x, y = int(data.split(","))
    #split data into three catagories

    if data != None or '':
        data = recvall(dataSize)
        #If data is found then run the recvieve all function
        if not data:
            return None
        frame = np.fromstring(data, dtype=np.uint8)
        return frame.reshape((y, x, 3))
        #Convert bytes to pixels and convert then from a 1D array to a 2D array

def sendData(direction, text, m):
    data = str(direction) + str(text)
    m.sendall(data)
