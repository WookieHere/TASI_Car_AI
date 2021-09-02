import threading
import time


class TimerInterrupt:
    def __init__(self, User_Interface, increment):
        self.t_prime = time.time()
        self.i = 0
        self.done = False
        self.increment = increment
        self.GH = User_Interface.GH           #stands for Graphics Handler
        self.UI = User_Interface
        self.start()
        """
           i: no. of iterations so far
           t_prime: next timer state
           done: status of program
           increment: time until next proc
        """

    def start(self):
        print("Initialized Timer Interrupt:")
        while(self.done == False):
            print("----------------------")
            print("i = ", self.i)
            self.i += 1
            self.UI.processInput()
            self.processGraphicsEvents()
            try:
                time.sleep(self.t_prime + self.increment - time.time())
            except (ValueError):
                print("Warning: Lag in timer handler")
            self.t_prime = time.time()

    def processGraphicsEvents(self):
        """this is just so I can have it run commands from the outside"""
        while self.GH.popEvent() != -1:
            pass

