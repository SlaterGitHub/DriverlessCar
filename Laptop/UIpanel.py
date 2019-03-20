import numpy as np
import cv2
import Tkinter as tk
from PIL import Image, ImageTk
from Tkinter import Text, END, DISABLED, NORMAL
from threading import Thread
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
import time
import DriverDB as db
import MergeSort as mg
"""import libraries"""

class UIpanel:
    def buildPanel(self):
        for l in range(len(self.content)):
            if self.panelType[l] == "Frame":
                image = tk.Frame(self.panel, width = self.x[l], height = self.y[l])
                image.grid(row = 0, column = 0)
                self.panelContent.append(tk.Label(image))
            elif self.panelType[l] == "Text":
                self.panelContent.append(tk.Text(self.panel, width = self.x[l], height = self.y[l]))
            elif self.panelType[l] == "Button":
                if self.content[l] == "Exit":
                    command = self.Exit
                elif self.content[l] == "Database":
                    command = self.DB
                elif self.content[l] == "All Drives":
                    command = self.getAllDrives
                elif self.content[l] == "Fails":
                    command = self.getFails
                elif self.content[l] == "Successes":
                    command = self.getSuccesses
                elif self.content[l] == "Start":
                    command = self.Start
                elif self.content[l] == "Success":
                    command = lambda:self. endProgram(False)
                elif self.content[l] == "Fail":
                    command = lambda: self.endProgram(True)
                elif self.content[l] == "Last Frame":
                    command = lambda button = l-10: self.showFrame(button)
                elif self.content[l][:4] == "Sort":
                    if self.content[l][5:] == "PK":
                        sorting = 0
                    elif self.content[l][5:] == "Time":
                        sorting = 1
                    elif self.content[l][5:] == "Distance":
                        sorting = 2
                    elif self.content[l][5:] == "Speed":
                        sorting = 3
                    command = lambda sortState =  sorting: self.sort(sortState)
                self.panelContent.append(tk.Button(self.panel, text = self.content[l], command = command, width = self.x[l], height = self.y[l]))
            elif self.panelType[l] == "Plot":
                self.fig = Figure(figsize=(self.x[l], self.y[l]))
                self.graph = self.fig.add_subplot(111)
                self.content[l][0] = np.array(self.content[l][0])
                self.content[l][1] = np.array(self.content[l][1])
                self.panel.axis, = self.graph.plot(self.content[l][1], self.content[l][0], color = 'blue')
                self.graph.set_ylabel(self.content[l][2])
                self.graph.set_xlabel(self.content[l][3])
                self.panel.graphPane = FigureCanvasTkAgg(self.fig, master = self.panel)
                self.panel.graphPane.get_tk_widget().place(x = self.loc[l][0], y = self.loc[l][1])
                self.ax = self.panel.graphPane.figure.axes[0]
                self.ax.set_xlim(0, 100)
                self.ax.set_ylim(0, 100)
                self.panelContent.append(self.panel.graphPane)
            else:
                print("UI error, panelType not compatible")
                return
            if self.panelType[l] != "Plot":
                self.panelContent[l].place(x = self.loc[l][0], y = self.loc[l][1])

    def setValue(self, Values):
        for l in range(len(Values)):
            if self.panelType[l] == "Plot":
                self.content[l][0] = np.array(Values[l][0])
                self.content[l][1] = np.array(Values[l][1])
            else:
                self.content[l] = Values[l]
        """If the value passed into the function is a value for a 
        plot then convert both items into numpy arrays"""
        

    def updateText(self, l):
        self.panelContent[l].config(state=NORMAL)
        self.panelContent[l].delete(1.0,END)
        self.panelContent[l].insert(END, self.content[l])
        self.panelContent[l].config(state=DISABLED)
        """Enable editing on the text field then change the 
        text to be clear then add the new value and finally 
        disable editing"""

    def updateFrame(self, l):
        img = cv2.cvtColor(self.content[l], cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(image=img)
        self.panelContent[l].imgtk = img
        self.panelContent[l].configure(image=img)
        """Convert the image in content to RGBA colour space
        then build the image from an array. Change the image 
        in imgtk to the new image"""

    def updatePlot(self, l):
        if self.content[l][0][len(self.content[l][0])-1] > 100:
            self.ax.set_xlim(0, int(self.content[l][0][len(self.content[l][0])-1])+2)
        self.panel.axis.set_data(self.content[l][0], self.content[l][1])
        self.panel.graphPane.draw()
        """If the maximum x plot is higher than the x axis limit then incrase the
        x axis limit to 2 more than the max x point.
        Set the graph to show the new numpy array and redraw the plot"""

    def displayValues(self):
        time.sleep(self.delay)
        if self.updating != 'drive' or 'database':
            for l in range(len(self.content)):
                if self.panelType[l] == "Frame":
                    self.updateFrame(l)
                elif self.panelType[l] == "Text":
                    self.updateText(l)
                elif self.panelType[l] == "Button":
                    self.panelType[l] = self.panelType[l]
                elif self.panelType[l] == "Plot":
                    self.updatePlot(l)
                else:
                    print("UI error, panelType not compatible")
                    return
        self.panel.after(20, self.displayValues)
        """Delay the update if the widgets are being changed then 
        run the update method depeinding on what the panelType is"""


    def showPanel(self):
        self.displayValues()
        self.panel.mainloop()
        """start the display values loop and show the window"""

    def __init__(self, xSize, ySize, content, panelType, loc):
        self.x = xSize
        self.y = ySize
        self.content = content
        self.panelType = panelType
        self.panelContent = []
        self.panel = tk.Tk()
        self.panel.geometry("1300x600")
        self.loc = loc
        self.updating = None
        self.closed = [False, False]
        self.databaseInfo = None
        self.delay = 0
        self.buildPanel()
        """Set the windows attributes and build the panel"""

    def DB(self):
        self.closed = [True, True]
        self.updating = 'database'
        self.delay = 0.2
        """Set closed to True True for True being closing 
        and True being for the drive has failed. Set panel status 
        to updating to database. While updating make the update method delay itself"""

    def getAllDrives(self):
        self.databaseInfo = db.getAll()
        """Get all rows from database"""

    def getFails(self):
        self.databaseInfo = db.getFoS(1)
        """Get only failed rows from database"""

    def getSuccesses(self):
        self.databaseInfo = db.getFoS(0)
        """Get only succeede rows from database"""

    def Start(self):
        self.updating = 'drive'
        self.delay = 0.2
        """set updating status to drive and make the update
        method delay itself"""

    def Exit(self):
        self.panel.destroy()
        self.updating = 'end'
        """close the entire panel and self the updating status to 
        end"""

    def update(self, xSize, ySize, content, panelType, loc):
        for l in self.panel.winfo_children():
            l.destroy()

        self.background = tk.Label(self.panel, bg="gray")
        self.background.place(x = 0, y = 0, width=1300, height=600)

        self.x = xSize
        self.y = ySize
        self.content = content
        self.panelType = panelType
        self.panelContent = []
        self.loc = loc
        self.buildPanel()
        self.updating = None
        self.delay = 0
        """Close all widgets and change the panels attributes befroe rebuilding the
        panel. Once panel is build change update status to None and have no delay in the 
        update method"""

    def isUpdating(self):
        return self.updating
        """Give updating variable to what calls it"""

    def endProgram(self, bool):
        self.closed = [True, bool]
        """Set closed to be True and either True or False"""

    def showFrame(self, l):
        frame = cv2.resize(self.databaseInfo[l][4], (800, 600), interpolation = cv2.INTER_AREA)
        cv2.imshow("Frame", frame)
        """Show the frame of row l in a seperate opencv window under the name 'frame'"""

    def sort(self, sortState):
        for m in range(len(self.databaseInfo)):
            for n in range(len(self.databaseInfo[0])-2):
                self.databaseInfo[m][n] = int(self.databaseInfo[m][n])
        self.databaseInfo = mg.sort(self.databaseInfo, sortState)
        """Change every item in the 0th to 3rd index to be an integer then
        pass the entire list through the merge sort with the sort state which is the
        cloumn of the data it should be sorted by"""
