import threading
import time


class TimerInterrupt:
    def __init__(self, increment):
        self.t_prime = time.time()
        #self.i = 0
        self.done = False
        self.increment = increment
        self.debugMode = False
        """
           i: no. of iterations so far
           t_prime: next timer state
           done: status of program
           increment: time until next proc
        """

    def setFrameRate(self, frameRate, debugmode = None):
        self.increment = 1/frameRate
        if debugmode != None:
            self.debugMode = debugmode

    def start(self):
        print("Initialized Timer Interrupt:")
        while(self.done == False):
            #print("----------------------")
            #print("i = ", self.i)
            #self.i += 1
            try:
                time.sleep(self.t_prime + self.increment - time.time())
            except (ValueError):
                print("Warning: Lag in timer handler")
            self.t_prime = time.time()

    def waitForFrame(self):
        try:
            time.sleep(self.t_prime + self.increment - time.time())
        except (ValueError):
            if self.debugMode:
                print("Warning: Lag in timer handler")
        self.t_prime = time.time()

    def updateFrame(self, Input):
        try:
            Input.processInput()
        except (AttributeError):
            print("ERROR: No Interface sent to Frame Control")

    def getMouse(self, Input):
        """this function only wants the coordinates at first"""
        mouseInput = "None"
        progressFlag = 0
        newCommand = ""
        Input.Msgr.Handler.window.checkMouse() #clear one mouse input
        cmdStartDict = {
            "makeWall" : "self.addObject(Wall(Point(",
            "makeTrackLine" : "self.addObject(TrackLine(Point(",
            "midCmd" : "),Point("
        }
        while mouseInput != "exit":

            if mouseInput[0] in cmdStartDict and progressFlag == 0:
                #newCommand = "self.addObject(Wall(Point(" + str(mouseInput[1].x) + "," + str(mouseInput[1].y) + "),Point("
                newCommand = cmdStartDict[mouseInput[0]]
                newCommand += str(mouseInput[1].x) + "," + str(mouseInput[1].y)
                newCommand += cmdStartDict["midCmd"]
                progressFlag = 1
            elif mouseInput[0] in cmdStartDict and progressFlag == 1:
                newCommand += (str(mouseInput[1].x) + "," + str(mouseInput[1].y) + ")))")
                progressFlag = 0
                return newCommand
            elif mouseInput[0] == "makeCar":
                newCommand = Input.createCar(mouseInput[1])
                return newCommand
            try:
                mouseInput = Input.checkMouseInput()
            except (AttributeError):
                print("ERROR: No Interface sent to Frame Control")
                return -1
        return -1

