import cv2
import Detection as detect
import Connection2 as cn
from threading import Thread
import time
import sys
import UIpanel
import DriverDB as db

command = None
connected = False
speed = "50"
key = None
frame = cv2.imread("C:\\Users\\Ryan\\Documents\\GitHub\\DriverlessCar\\Laptop\\blackPhoto.png", 3)
x = None
y = None
StartUI = [[10, 10, 10], [3, 3, 3],["Database", "Start", "Exit"],["Button", "Button", "Button"],[[1000, 540], [1100, 540], [1200, 540]]]
DriveUI = [[800, 10, 10, 10, 40, 40, 40, 4.5],[600, 3, 3, 3, 1, 1, 1, 4],[frame, "Database", "Fail", "Success", "Time", "Distance", "Speed", [x, y, "speed", "time"]],["Frame", "Button", "Button", "Button", "Text", "Text", "Text", "Plot"],[[0,0], [1000, 540], [1100, 540], [1200, 540], [804, 10], [804, 50], [804, 90], [810, 130]]]
DatabaseUI = [[140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4], ["", "", "", "", "", "", "", "", "", "", "Start", "Start", "Start", "Start", "Start", "Start", "Start", "Start", "Start", "Start", "All Drives", "Fails", "Successes"], ["Text", "Text", "Text", "Text", "Text", "Text", "Text", "Text", "Text", "Text", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button"], [[0, 100], [0, 150], [0, 200], [0, 250], [0, 300], [0, 350], [0, 400], [0, 450], [0, 500], [0, 550], [1175, 97], [1175, 147], [1175, 197], [1175, 247], [1175, 297], [1175, 347], [1175, 397], [1175, 447], [1175, 497], [1175, 547], [20, 15], [220, 15], [420, 15]]]

HomeUI = UIpanel.UIpanel(StartUI[0], StartUI[1], StartUI[2], StartUI[3], StartUI[4])

UI = Thread(target = HomeUI.showPanel).start()

def drive():
    global DriveUI, frame
    progtime = time.time()
    if connected == False:
        pipeline3, pipeline2, pipeline1 = cn.getConnection()
        connected == True

    recvSign = Thread(target = cn.recvTextFrame)
    #Always look for a speed sign being sent from the raspberry pi
    recvSign.start()
    #cn.setConnection()

    HomeUI.update(DriveUI[0], DriveUI[1], DriveUI[2], DriveUI[3], DriveUI[4])

    while True:
        frame = cn.recvVarFrame(pipeline3, False)
        speed, distance = cn.recvStats(pipeline2)
        if (frame is not None):
            DriveUI[2][0] = cv2.resize(frame, (800, 600), interpolation = cv2.INTER_AREA)
            DriveUI[2][4] = "Time:" + ("%.2f" % (time.time() - progtime))
            DriveUI[2][5] = "Distance: " + str(distance)
            DriveUI[2][6] = "Speed: " + str(speed)
            HomeUI.setValue(DriveUI[2])

        key = cv2.waitKey(1) & 0xFF
        if (key == ord('q')) or (HomeUI.closed == [True, True]):
            cn.sendData("FL")
            break
        elif (key == ord('e')) or (HomeUI.closed == [True, False]):
            cn.sendData("SS")
            break

    time.sleep(0.1)

    finalFrame, finalDistance, finalSpeed, progDuration, fail = cn.recvFinals()
    print(finalDistance)
    print(finalSpeed)
    print(progDuration)
    print(fail)

    db.upload(int(progDuration), int(finalDistance), int(finalSpeed), int(fail), finalFrame)

def database():
    global DatabaseUI
    HomeUI.update(DatabaseUI[0], DatabaseUI[1], DatabaseUI[2], DatabaseUI[3], DatabaseUI[4])
    while True:
        time.sleep(0.2)
        databaseContent = HomeUI.databaseInfo
        if databaseContent != None:
            dataLength = len(databaseContent)
            if dataLength >= 10:
                for x in range(10):
                    DatabaseUI[2][x] = "Drive ID: " + str(databaseContent[x][0]) + ", " + "Program Time " + str(databaseContent[x][1]) + ", " + "Last Distance Recorded " + str(databaseContent[x][2]) + ", " + "Last Speed Recorded " + str(databaseContent[x][3])
            else:
                for x in range(dataLength):
                    DatabaseUI[2][x] = "Drive ID: " + str(databaseContent[x][0]) + ", " + "Program Time " + str(databaseContent[x][1]) + ", " + "Last Distance Recorded " + str(databaseContent[x][2]) + ", " + "Last Speed Recorded " + str(databaseContent[x][3])
                for x in range(dataLength, 10):
                    DatabaseUI[2][x] = ""
            HomeUI.setValue(DatabaseUI[2])

def end():
    cv2.destroyAllWindows()
    sys.exit()

while True:
    if (command != HomeUI.updating) and (HomeUI.updating != None):
        command = HomeUI.updating
        globals()[command]()
