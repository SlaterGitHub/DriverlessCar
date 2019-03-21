import cv2
import numpy as np
import imutils

StopPth = 'C:\\Users\\Ryan\\Documents\\GitHub\\DriverlessCar\\RaspberryPi\\stopsign_classifier.xml'
SpeedPth = "C:\\Users\\Ryan\\Documents\\GitHub\\DriverlessCar\\RaspberryPi\\Speedlimit_HAAR_ 13Stages.xml"
StopCas = cv2.CascadeClassifier(StopPth)
SpeedCas = cv2.CascadeClassifier(SpeedPth)
"""Set the path to the cascade filters"""

boundries = [([50, 30, 20], [100, 250, 150])]
"""Set the boundaries of the colour that the road can be"""

averageX = None
"""Make averageX None to being with"""

def getPath(frame, grey):
    global averageX
    global boundries
    for (lower, upper) in boundries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")
        """Convert the boundaries to an 8 bit integer"""

        TrimFrame = np.array(frame[200:210, 0:320], dtype = "uint8")
        TrimGrey = np.array(grey[200:210, 0:320], dtype = "uint8")
        """Get only the section fo the frame that needs to be scanned"""

        mask = cv2.inRange(TrimFrame, lower, upper)
        mask2 = cv2.erode(mask, None, iterations = 2)
        mask2 = cv2.dilate(mask2, None, iterations = 2)
        """apply masks that get rid of any pixels that don't fit into the colour boundries"""

        contours = cv2.findContours(mask2.copy(),
                                    cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
        contours = contours[1] if imutils.is_cv2() else contours[0]
        """make an array of each block of colour, this is pixels that are touching"""

        centers = []
        x = [None]*2
        y = [None]*2
        if contours is not None:
            length = len(contours)
        else:
            length = 0
        """make an empty x and y array of size 2 and find the length of the list contours"""

        if length > 1:
            for i in range(2):
                MaxContour = max(contours, key=cv2.contourArea)
                """find the biggest item in the contours array"""

                try:
                    Moments = cv2.moments(MaxContour)
                    """get the y, x, w, h value of the contour"""

                    centers.append((int(Moments["m10"] / Moments["m00"]),
                                    int(Moments["m01"] / Moments["m00"])))
                    """add that contour to a list of centers"""

                    contours.remove(MaxContour)
                    """remove biggest contour from array"""

                    x[i], y[i] = centers[i]
                    """get the x and y value of the center of the biggest contour"""

                    if i == 1:
                        averageX = int((x[0]+x[1])/2)
                        """calculate the average x value of the 2 biggest contours"""

                except ValueError:
                    averageX = None
        else:
            averageX = None

        inBound = cv2.bitwise_or(TrimFrame, TrimFrame, mask = mask2)
        """find the pixels that are inbound to the boudries"""

        greyBackground = cv2.cvtColor(TrimGrey, cv2.COLOR_GRAY2BGR)
        """make the grey frame a BGR colour space"""

        mask = cv2.bitwise_not(mask)
        """find pixels out of bound"""

        outBound = np.full(TrimFrame.shape, greyBackground, dtype = np.uint8)
        """change out of bound pixels to the grey version of themselves"""

        background = cv2.bitwise_or(outBound, outBound, mask = mask)
        output = cv2.bitwise_or(inBound, background)
        """combine the inbound and out bound pixels"""

        frame[200:210, 0:320] = output
        """replace the pixels of the section in frame with the processed ones"""

        return frame, averageX

def getSign(frame, Casc):
    for (x, y, w, h) in Casc:
        cv2.rectangle(frame, (x, y), (x+y, y+h), (0, 255, 0), 3)
    return frame
    """use the location data of any signs and draw them on the frame in a rectangle"""

def setCascFilter(frame):
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    """convert the image to greyscale"""
    stopSigns = StopCas.detectMultiScale(
    grey,
    scaleFactor=1.1,
    minNeighbors=2,
    minSize=(60, 75),
    flags=cv2.CASCADE_SCALE_IMAGE
    )
    """define the rules for the cascde classifier, the sensitivity, minimum resolution and classifier type"""
    speedSigns = SpeedCas.detectMultiScale(
        grey,
        scaleFactor=1.1,
        minNeighbors=4,
        minSize=(50, 50),
        flags=cv2.CASCADE_SCALE_IMAGE
        )
    """define the rules for the cascde classifier, the sensitivity, minimum resolution and classifier type"""
    return stopSigns, speedSigns, grey
