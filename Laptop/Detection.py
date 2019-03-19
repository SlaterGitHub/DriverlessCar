import cv2
import os
from pytesseract import image_to_string
import numpy as np
import imutils
from PIL import Image
import re
from time import sleep
"""import libraries"""

def getText(grey):
    filename = "{}.png".format(os.getpid())
    #create a file with a avalile number
    cv2.imwrite(filename, grey)
    #write the array of pixels to the file
    textDetection = image_to_string(Image.open(filename))
    #run the file through the text detection tesseract

    if textDetection != None or '':
        os.remove(filename)
        textDetection = speedCheck(textDetection)
        return textDetection
    else:
        os.remove(filename)
    #remove file
    """create a file of a unique number and write the image to it, pass the file
    through the pytesseract to return a string, if a string is returned remove
    the file and pass it through speedCheck to get a number"""

def speedCheck(text):
    text = re.search(r'\d+', text)
    if text != None or '':
        return text.group()
    return ''
    """Use regular expression to find the first number in the string"""
