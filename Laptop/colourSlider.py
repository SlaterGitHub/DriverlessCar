from Tkinter import *
from time import sleep
from threading import Thread
import cv2
import numpy as np

master = Tk()

r = Scale(master, from_=0, to=255, length=510, orient=HORIZONTAL)
r.pack()
r2 = Scale(master, from_=0, to=255, length=510, orient=HORIZONTAL)
r2.pack()
b = Scale(master, from_=0, to=255, length=510, orient=HORIZONTAL)
b.pack()
b2 = Scale(master, from_=0, to=255, length=510, orient=HORIZONTAL)
b2.pack()
g = Scale(master, from_=0, to=255, length=510, orient=HORIZONTAL)
g.pack()
g2 = Scale(master, from_=0, to=255, length=510, orient=HORIZONTAL)
g2.pack()

r.set(255)
g.set(255)
b.set(255)

myThread = Thread(target = mainloop)

myThread.start()

video = cv2.VideoCapture(0)

sleep(0.2)

while True:
    ret, frame = video.read()
    frame = cv2.resize(frame, (80, 60), interpolation = cv2.INTER_AREA)
    w, h = frame.shape[:2]
    for x in range(h):
        for y in range(w):
            maxV = max(frame[y][x])
            indx = np.where(frame[y][x] == maxV)
            frame[y][x] = [0, 0, 0]
            frame[y][x][indx] = maxV

    rd = int(r.get())
    gn = int(g.get())
    be = int(b.get())
    rd2 = int(r2.get())
    gn2 = int(g2.get())
    be2 = int(b2.get())

    if rd > rd2:
        buffer = rd
        rd = rd2
        rd2 = buffer
    if gn > gn2:
        buffer = gn
        gn = gn2
        gn2 = buffer
    if be > be2:
        buffer = be
        be = be2
        be2 = buffer

    boundries = [([be, gn, rd], [be2, gn2, rd2])]

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for (lower, upper) in boundries:
        lower = np.array(lower, dtype = "uint8")
        upper = np.array(upper, dtype = "uint8")

        mask = cv2.inRange(frame, lower, upper)
        mask2 = cv2.erode(mask, None, iterations = 2)
        mask2 = cv2.dilate(mask2, None, iterations = 2)

        inBound = cv2.bitwise_or(frame, frame, mask = mask2)
        greyBackground = cv2.cvtColor(grey, cv2.COLOR_GRAY2BGR)
        mask = cv2.bitwise_not(mask)
        outBound = np.full(frame.shape, greyBackground, dtype = np.uint8)
        background = cv2.bitwise_or(outBound, outBound, mask = mask)
        output = cv2.bitwise_or(inBound, background)


    output = cv2.resize(output, (640, 480), interpolation = cv2.INTER_AREA)

    cv2.imshow("colours", output)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
master.quit()
