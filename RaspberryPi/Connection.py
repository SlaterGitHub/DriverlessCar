import socket
import numpy
import lz4.frame
socketNum = 5001
socketNum2 = 6001
ip = "localhost"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
speed = "50"

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

    #Connect to server side of socket
    return speedFrame, speedText

def recvData():
    while True:
        speed = r.recv(2)
        #Recvieve 2 bytes of data, long enough to recieve speeds like 50 or 20
        if speed != None or '':
            speed = 1.0 / float(data)
            #If no data is recvieved return nothing
            #By making speed an inverse,
            #the higher the number on the sign the lower the inverse number will be

def getSpeed():
    data = speedText.recv(2)
    if data != None or '':
        speed = data.decode()
        return speed
    return speed

def sendData(frame, c):
    reso = frame.shape[1]
    frame = frame.flatten()
    #Convert frame from a 2D array to a 1D array
    datas = frame.tostring()
    datas = lz4.frame.compress(datas)
    size = str(len(datas))
    for x in range(6-len(size)):
        size = "," + size
    for x in range(3-len(reso)):
        reso = "," + reso
    c.sendall(size+reso+datas)
    return
    #Convert to a string form and send the entire frame
