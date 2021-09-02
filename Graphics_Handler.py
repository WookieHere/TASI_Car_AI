import math
from graphics import *



class GHandler:
    def __init__(self):
        self.window = GraphWin('Car_AI', 1000, 1000)
        self.Objects = []
        self.UserObjects = []
        self.event_queue = []
        """that array will be filled later with things to draw etc."""



    def addObject(self, object):
        """object is a string of the init call"""
        pre_string = "self.Objects.append(" + object + ")"
        exec(pre_string)
        self.Objects[len(self.Objects) - 1].draw(self.window)   #this draws the newly placed object

    def addUserObject(self, object):
        """object is a string of the init call"""
        pre_string = "self.UserObjects.append(" + object + ")"
        exec(pre_string)
        self.UserObjects[len(self.UserObjects) - 1].draw(self.window)  # this draws the newly placed object

    def addToEvents(self, event):
        if event == "end":
            self.event_queue.append(event)
        else:
            for x in self.UserObjects:
                x.addToActionQueue(event)

    def popEvent(self):
        """this will process an event and then do the appropriate command"""
        try:
            if self.event_queue[0] == "end":
                for x in self.Objects:
                    x.act()
                for x in self.UserObjects:
                    x.act()
                self.event_queue.pop()
                return -1
                """this does not execute an 'end frame' command"""
            else:
                exec(self.event_queue[0])
                self.event_queue.pop()
                return 0
        except (IndexError):
            print("Warning: Event Queue is empty")
            self.event_queue.append("end")
            for x in self.Objects:
                x.act()
            for x in self.UserObjects:
                x.act()
            self.event_queue.pop()
            return -1

