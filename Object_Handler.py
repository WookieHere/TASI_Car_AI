from graphics import *
import math

"""This file is for abstract object classes"""

class Object:
    def __init__(self):
        self.name = "abstract"
        self.err = Rectangle(Point(10, 10), Point(50, 50))
        self.err.setFill('red')

    def draw(self, window):
        print("ERROR: Blank object class present in graphics handler")

    def act(self):
        print("ERROR: Blank object class present in graphics handler")

class UserObject(Object):
    def __init__(self):
        self.name = "abstract"
        self.actQueue = []

    def addToActionQueue(self, action):
        """action is a string for the action to be added"""
        self.actQueue.append(action)

    def act(self):
        for x in self.actQueue:
            try:
                exec(x)
            except UNSUPPORTED_METHOD:
                print("Warning: Command " + x + " Could not be executed")
            self.actQueue.remove(x)