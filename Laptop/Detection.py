import cv2
import os
from pytesseract import image_to_string
import numpy as np
import imutils
from PIL import Image

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
