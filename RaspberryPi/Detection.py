import cv2
import numpy as np
import imutils

StopPth = 'C:\\Users\\Ryan\\Documents\\GitHub\\DriverlessCar\\RaspberryPi\\stopsign_classifier.xml'
SpeedPth = "C:\\Users\\Ryan\\Documents\\GitHub\\DriverlessCar\\RaspberryPi\\Speedlimit_HAAR_ 13Stages.xml"
StopCas = cv2.CascadeClassifier(StopPth)
SpeedCas = cv2.CascadeClassifier(SpeedPth)
#boundries = [([230, 230, 230], [255, 255, 255])]
#For red hair
boundries = [([0, 0, 150], [200, 200, 255])]

def getPath(frame, grey):
    for (lower, upper) in boundries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        #convert upper and lower boundries into pixel format

        TrimFrame = np.array(frame[200:210, 0:320], dtype = "uint8")
        TrimGrey = np.array(grey[200:210, 0:320], dtype = "uint8")
        #get a section of the frame and grey frame

        mask = cv2.inRange(TrimFrame, lower, upper)
        mask2 = cv2.erode(mask, None, iterations = 2)
        mask2 = cv2.dilate(mask2, None, iterations = 2)
        #apply masks that get rid of any pixels that don't fit into the colour boundries

        contours = cv2.findContours(mask2.copy(),
                                    cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if imutils.is_cv2() else contours[1]
        #make an array of each block of colour, this is pixels that are touching
        centers = []
        x = [None]*2
        y = [None]*2
        length = len(contours)
        #make an empty x and y array of size 2 and find the length of the list contours

        if length > 1:
            for i in range(2):
                MaxContour = max(contours, key=cv2.contourArea)
                #find the biggest item in the contours array
                try:
                    #ContourIndx = contours.index(MaxContour)
                    #get the index of the biggest item
                    Moments = cv2.moments(MaxContour)
                    #get the y, x, w, h value of the contour
                    centers.append((int(Moments["m10"] / Moments["m00"]),
                                    int(Moments["m01"] / Moments["m00"])))
                    #add that contour to a list of centers
                    contours.remove(MaxContour)
                    #remove biggest contour from array
                    x[i], y[i] = centers[i]
                    #get the x and y value of the center of the biggest contour
                    if i == 1:
                        averageX = (x[0]+x[1])/2
                        #calculate the average x value of the 2 biggest contours
                except ValueError:
                    print("Value Error")
                    averageX = None

        inBound = cv2.bitwise_or(TrimFrame, TrimFrame, mask = mask2)
        #find the pixels that are inbound to the boudries
        greyBackground = cv2.cvtColor(TrimGrey, cv2.COLOR_GRAY2BGR)
        #make the grey frame a BGR colour space
        mask = cv2.bitwise_not(mask)
        #find pixels out of bound
        outBound = np.full(TrimFrame.shape, greyBackground, dtype = np.uint8)
        #change out of bound pixels to the grey version of themselves
        background = cv2.bitwise_or(outBound, outBound, mask = mask)
        output = cv2.bitwise_or(inBound, background)
        #combine the inbound and out bound pixels

        frame[200:210, 0:320] = output
        #replace the pixels of the section in frame with the processed ones

        try:
            return frame, averageX
        except:
            return None, None

def getSign(frame, Casc):
    for (x, y, w, h) in Casc:
        cv2.rectangle(frame, (x, y), (x+y, y+h), (0, 255, 0), 3)
    return frame

def setCascFilter(frame):
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    stopSigns = StopCas.detectMultiScale(
    grey,
    scaleFactor=1.1,
    minNeighbors=2,
    minSize=(60, 75),
    flags=cv2.CASCADE_SCALE_IMAGE
    )
    speedSigns = SpeedCas.detectMultiScale(
        grey,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(50, 50),
        flags=cv2.CASCADE_SCALE_IMAGE
        )
    return stopSigns, speedSigns, grey
