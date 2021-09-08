import threading
import time


class TimerInterrupt:
    def __init__(self, increment):
        self.t_prime = time.time()
        #self.i = 0
        self.done = False
        self.increment = increment
        """
           i: no. of iterations so far
           t_prime: next timer state
           done: status of program
           increment: time until next proc
        """

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

    def waitForFrame(self, DebugMode = False):
        try:
            time.sleep(self.t_prime + self.increment - time.time())
        except (ValueError):
            if DebugMode:
                print("Warning: Lag in timer handler")
        self.t_prime = time.time()

    def updateFrame(self, Input):
        try:
            Input.processInput()
        except (AttributeError):
            print("ERROR: No Interface sent to Frame Control")

    def getMouse(self, Input):
        """this function only wants the coordinates at first"""
        mouseInput = None
        progressFlag = 0
        newCommand = ""
        while mouseInput != -1:

            if mouseInput != None and progressFlag == 0:
                newCommand = "self.addObject(Wall(Point(" + str(mouseInput.x) + "," + str(mouseInput.y) + "),Point("
                progressFlag = 1
            elif mouseInput != None and progressFlag == 1:
                newCommand += (str(mouseInput.x) + "," + str(mouseInput.y) + ")))")
                progressFlag = 0
                return newCommand
            try:
                mouseInput = Input.checkMouseInput()
            except (AttributeError):
                print("ERROR: No Interface sent to Frame Control")
                return -1
        return -1



"""
    def processGraphicsEvents(self):
        #this is just so I can have it run commands from the outside
        while self.GH.popEvent() != -1:
            pass
"""
