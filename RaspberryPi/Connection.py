import socket
import numpy
socketNum = 5001
socketNum2 = 6001
ip = "localhost"
dataSize = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def setConnection():
    s.bind(("localhost", (socketNum)))
    #Create a server side socket
    print("binded")
    s.listen(10)
    #Wait for a recieving side to connect
    c, addr = s.accept()
    #set socket to c when recieving side connects

    r.connect((ip, socketNum2))
    #Connect to server side of socket
    return c, r

"""def getConnection():
    r.connect((ip, socketNum2))
    return r"""

def recvData():
    while True:
        speed = r.recv(2)
        #Recvieve 2 bytes of data, long enough to recieve speeds like 50 or 20
        if not speedDirect:
            return None, None
            #If no data is recvieved return nothing
        speed = 1.0 / float(speed)
        #By making speed an inverse,
        #the higher the number on the sign the lower the inverse number will be
        return speed

def sendData(frame, c):
    frame = frame.flatten()
    #Convert frame from a 2D array to a 1D array
    datas = frame.tostring()
    c.sendall(datas)
    #Convert to a string form and send the entire frame
