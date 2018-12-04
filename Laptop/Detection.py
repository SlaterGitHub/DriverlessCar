import cv2
import os
from pytesseract import image_to_string
import numpy as np
import imutils
from PIL import Image
from time import sleep

StopPth = 'C:\Users\Ryan\Documents\Python Work\DriverlessCar\Laptop\stopsign_classifier.xml'
SpeedPth = "\Users\\Ryan\\Documents\\Python Work\\DriverlessCar\\Laptop\\Speedlimit_HAAR_ 13Stages.xml"
StopCas = cv2.CascadeClassifier(StopPth)
SpeedCas = cv2.CascadeClassifier(SpeedPth)
#boundries = [([230, 230, 230], [255, 255, 255])]
#For red hair
boundries = [([0, 0, 180], [150, 150, 255])]

def getPath(frame, grey):
    for (lower, upper) in boundries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

        TrimFrame = np.array(frame[200:210, 0:320], dtype = "uint8")
        TrimGrey = np.array(grey[200:210, 0:320], dtype = "uint8")

        mask = cv2.inRange(TrimFrame, lower, upper)
        mask2 = cv2.erode(mask, None, iterations = 2)
        mask2 = cv2.dilate(mask2, None, iterations = 2)

        contours = cv2.findContours(mask2.copy(),
                                    cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[0] if imutils.is_cv2() else contours[1]
        centers = []
        x = [None]*2
        y = [None]*2
        length = len(contours)

        if length > 1:
            for i in range(2):
                MaxContour = max(contours, key=cv2.contourArea)
                try:
                    ContourIndx = contours.index(MaxContour)
                    Moments = cv2.moments(MaxContour)
                    centers.append((int(Moments["m10"] / Moments["m00"]),
                                    int(Moments["m01"] / Moments["m00"])))
                    del contours[int(ContourIndx)]
                    contourIndx = 0
                    x[i], y[i] = centers[i]
                    if i == 1:
                        averageX = (x[0]+x[1])/2
                except ValueError:
                    print("Value Error")

        inBound = cv2.bitwise_or(TrimFrame, TrimFrame, mask = mask2)
        greyBackground = cv2.cvtColor(TrimGrey, cv2.COLOR_GRAY2BGR)
        mask = cv2.bitwise_not(mask)
        outBound = np.full(TrimFrame.shape, greyBackground, dtype = np.uint8)
        background = cv2.bitwise_or(outBound, outBound, mask = mask)
        output = cv2.bitwise_or(inBound, background)

        frame[200:210, 0:320] = output

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
    cv2.waitKey(1)
    return stopSigns, speedSigns, grey

def getText(grey):
    filename = "{}.png".format(os.getpid())
    #create a file with a avalile number
    cv2.imwrite(filename, grey)
    #write the array of pixels to the file
    textDetection = image_to_string(Image.open(filename))
    #run the file through the text detection tesseract

    if textDetection != None or '':
        os.remove(filename)
        return textDetection
    else:
        os.remove(filename)
    #remove file

def setTextFilter(grey):
    grey = cv2.medianBlur(grey, 3)
    return grey
