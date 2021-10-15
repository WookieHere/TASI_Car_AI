from Car_Handler import *



class GHandler:
    def __init__(self, xsize = 1000, ysize = 1000):
        self.window = GraphWin('Car_AI', xsize, ysize)
        self.Objects = []
        self.UserObjects = []
        self.event_queue = []
        """that array will be filled later with things to draw etc."""

    def addObject(self, object):
        """object is a string of the init call"""
        try:
            pre_string = "self.Objects.append(" + object + ")"
            exec(pre_string)
        except (TypeError):
            self.Objects.append(object)

        self.Objects[len(self.Objects) - 1].draw(self.window)   #this draws the newly placed object

    def addUserObject(self, object):
        """object is a string of the init call"""
        try:
            pre_string = "self.UserObjects.append(" + object + ")"
            exec(pre_string)
        except (TypeError):
            self.UserObjects.append(object)
        self.UserObjects[len(self.UserObjects) - 1].draw(self.window)  # this draws the newly placed object

    def addToEvents(self, event):
        if event == "end":
            self.event_queue.append(event)
        else:
            for x in self.UserObjects:
                x.addToActionQueue(event)

    def setEvents(self, message):
        """the message is an array of strings as commands to particular objects"""
        self.event_queue = message
        pass

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

    def getObjects(self):
        return self.Objects

    def getUserObjects(self):
        return self.UserObjects

    def popAllEvents(self):
        while len(self.event_queue) > 0:
            try:
                if self.event_queue[0] == "end":
                    for x in self.Objects:
                        x.act()
                    for x in self.UserObjects:
                        x.act()
                    self.event_queue.pop(0)
                    """this does not execute an 'end frame' command"""
                else:
                    for x in self.UserObjects:
                        x.sendCmd(self.event_queue[0])
                    exec(self.event_queue[0])
                    self.event_queue.pop(0)
            except (IndexError, AttributeError):
                self.event_queue.pop(0)

    def drawPointCloud(self, pointcloud):
        for pt in pointcloud:
            temp = Circle(Point(pt.x, pt.y), 5)
            temp.setFill('blue')
            temp.draw(self.window)