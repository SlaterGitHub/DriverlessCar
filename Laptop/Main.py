import cv2
import Detection as detect
import Connection2 as cn
from threading import Thread
import time
import sys
import UIpanel
import DriverDB as db
"""import libraries"""

x = [1]
y = [0]
command = None
connected = False
speed = "50"
key = None
"define variables"

frame = cv2.imread("C:\\Users\\Ryan\\Documents\\GitHub\\DriverlessCar\\Laptop\\blackPhoto.png", 3)
"""Set frame to be a black image to start off with, this allows the GUI to have
somthing to build around until a full frame is sent by the raspberry pi"""

StartUI = [[10, 10, 10], [3, 3, 3],["Database", "Start", "Exit"],["Button", "Button", "Button"],[[1000, 540], [1100, 540], [1200, 540]]]
DriveUI = [[800, 10, 10, 10, 40, 40, 40, 4.5],[600, 3, 3, 3, 1, 1, 1, 4],[frame, "Database", "Fail", "Success", "Time", "Distance", "Speed", [x, y, "speed", "time"]],["Frame", "Button", "Button", "Button", "Text", "Text", "Text", "Plot"],[[0,0], [1000, 540], [1100, 540], [1200, 540], [804, 10], [804, 50], [804, 90], [810, 130]]]
DatabaseUI = [[140, 140, 140, 140, 140, 140, 140, 140, 140, 140, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 15, 15, 15, 15, 10, 10, 10, 10], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4], ["", "", "", "", "", "", "", "", "", "", "Last Frame", "Last Frame", "Last Frame", "Last Frame", "Last Frame", "Last Frame", "Last Frame", "Last Frame", "Last Frame", "Last Frame", "All Drives", "Fails", "Successes", "Exit", "Sort PK", "Sort Time", "Sort Distance", "Sort Speed"], ["Text", "Text", "Text", "Text", "Text", "Text", "Text", "Text", "Text", "Text", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button", "Button"], [[0, 100], [0, 150], [0, 200], [0, 250], [0, 300], [0, 350], [0, 400], [0, 450], [0, 500], [0, 550], [1175, 97], [1175, 147], [1175, 197], [1175, 247], [1175, 297], [1175, 347], [1175, 397], [1175, 447], [1175, 497], [1175, 547], [20, 15], [220, 15], [420, 15], [620, 15], [820, 15], [920, 15], [1020, 15], [1120, 15]]]
"""Define the GUI's 3 states, to make any widget in the GUI the x size, y size,
content, widget type and location has to be given"""

HomeUI = UIpanel.UIpanel(StartUI[0], StartUI[1], StartUI[2], StartUI[3], StartUI[4])
"""Build the initial GUI with the StartUI widgets"""

UI = Thread(target = HomeUI.showPanel).start()
"""because tkinter take the entire thread its in to show the panel, it must be
run in a seperate thread"""

def drive():
    global DriveUI, frame
    progtime = time.time()
    if connected == False:
        pipeline3, pipeline2, pipeline1 = cn.getConnection()
        connected == True
    """Get the current time once the drive starts and connect to the rapberry
    pi. Once connected set connected to true"""

    recvSign = Thread(target = cn.recvTextFrame)
    recvSign.start()
    """Constantly check for speed signs with a seperae thread"""

    HomeUI.update(DriveUI[0], DriveUI[1], DriveUI[2], DriveUI[3], DriveUI[4])
    """change the GUI widgets to now display the DriveUI instead fo the StartUI"""

    while True:
        frame = cn.recvVarFrame(pipeline3, False)
        speed, distance = cn.recvStats(pipeline2)
        """recieve a full frame, speed and distance from raspberry pi"""

        if (frame is not None) and (speed != None) and (distance != None):
            DriveUI[2][0] = cv2.resize(frame, (800, 600), interpolation = cv2.INTER_AREA)
            DriveUI[2][4] = "Time:" + ("%.2f" % (time.time() - progtime))
            DriveUI[2][5] = "Distance: " + str(distance)
            DriveUI[2][6] = "Speed: " + str(speed)
            if max(x) != int(time.time() - progtime):
                x.append(int(time.time() - progtime))
                y.append(int(speed))
            DriveUI[2][7][0] = x
            DriveUI[2][7][1] = y
            HomeUI.setValue(DriveUI[2])
        """Resize the frame to be upscaled from 320x240 to 800x600. Change the
        content of the DriveUI to have the new frame, time, distance and change
        in time since start of the drive. Before adding a new plot to the graph,
        make sure that there isnt already a plot in the same location of x and
        if there is skip the entire step. Finally take the enitre content
        section of DriveUI and put it into the GUI"""

        key = cv2.waitKey(1) & 0xFF
        if (key == ord('q')) or (HomeUI.closed == [True, True]):
            cn.sendData("FL")
            break
        elif (key == ord('e')) or (HomeUI.closed == [True, False]):
            cn.sendData("SS")
            break
        """If q or The Fail button is pressed send 'FL' to the raspberry pi to
        tell it that it has failed the drive. If e or The Success button is
        pressed senf 'SS' to the raspberry pi to tell it that it has succeed the
        drive. Then break the loop"""

    time.sleep(0.1)

    finalFrame, finalDistance, finalSpeed, progDuration, fail = cn.recvFinals()

    db.upload(int(progDuration), int(finalDistance), int(finalSpeed), int(fail), finalFrame)
    """Wait 100ms for the raspberry pi to send the final data and recieve it all
    from recvFinals, then upload the data to the database"""

def database():
    global DatabaseUI
    HomeUI.update(DatabaseUI[0], DatabaseUI[1], DatabaseUI[2], DatabaseUI[3], DatabaseUI[4])
    """Change GUI to have content for DatabaseUI"""

    while True:
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
    """Get the database content and check if it is not empty, if not then get
    the amount of rows in the database. If there are more than 9 rows, change
    the content section of the database to be the first 10 rows. If there are
    less than 10 rows then change the content section to all the rows and any
    unfilled sections to be empty"""

def end():
    cv2.destroyAllWindows()
    sys.exit()
    """Once the program ends, close all OpenCV windows and exit the program"""

while True:
    if (command != HomeUI.updating) and (HomeUI.updating != None):
        command = HomeUI.updating
        globals()[command]()
        """Once HomeUI.updating changes and is not None run the command as the
        name of a method"""
