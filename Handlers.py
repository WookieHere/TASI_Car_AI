import _pickle
from Car_Handler import *

class Handler:
    def __init__(self):
        """This is an abstract class"""
        self.Objects = []
        self.UserObjects = []
        self.event_queue = []
        self.iteration_count = 0
        self.save_file = open("car_network.obj", "rb")


    def getObjects(self):
        return self.Objects

    def incIterations(self):
        self.iteration_count += 1

    def getUserObjects(self):
        return self.UserObjects

    def setEvents(self, message):
        """the message is an array of strings as commands to particular objects"""
        self.event_queue = message
        pass


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

    def addObject(self, object):
        """object is a string of the init call"""
        try:
            pre_string = "self.Objects.append(" + object + ")"
            exec(pre_string)
        except (TypeError):
            self.Objects.append(object)

    def addUserObject(self, object):
        """object is a string of the init call"""
        try:
            pre_string = "self.UserObjects.append(" + object + ")"
            exec(pre_string)
        except (TypeError):
            self.UserObjects.append(object)

    def save(self, obj):
        try:
            self.save_file = open("car_network.obj", "wb")
            network = obj.pullNetwork()
            _pickle.dump(network, self.save_file, _pickle.HIGHEST_PROTOCOL)
        except (AttributeError):
            print("Error: Unable to save network")
            pass

    """Save and load are incomplete, but exportNetwork() works!"""
    def load(self):
        try:
            self.save_file = open("car_network.obj", "rb")
            network = _pickle.load(self.save_file)
            obj.setNetwork(network)
        except (AttributeError):
            pass

class PhysicalHandler(Handler):
    def __init__(self):
        super().__init__()
        self.funcDict = {
            "self.changeSpeed(1)" : "self.moveMotor(1)",
            "self.changeSpeed(-1)": "self.moveMotor(-1)",
            "self.changeDir(1)": "self.changeTurnRate(1)",
            "self.changeDir(-1)": "self.changeTurnRate(-1)",
            "pass" : "pass"
        }

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
                    exec(self.funcDict[self.event_queue[0]])
                    self.event_queue.pop(0)
            except (IndexError, AttributeError):
                self.event_queue.pop(0)

    def moveMotor(self, always_high_bool):
        """
        This is for Jon/Hrishi to make
        the input parameter is always 1 or -1
        this is for forward/backwards
        """
        pass

    def changeTurnRate(self, always_high_bool):
        """
        This is for Jon/Hrishi to make
        the input parameter is always 1 or -1
        this is for left/right wheel turn
        """
        pass

    def getPointCloud(self):
        pointcloud = []
        """
        This is for the Lidar input in the real world
        """
        return pointcloud

class HeadlessHandler(Handler):
    def __init__(self):
        super().__init__()
        self.iteration_len = 0

    def setRunLength(self, num):
        self.iteration_len = num

    def popAllEvents(self):
        super().popAllEvents()
        if self.iteration_len < self.iteration_count:
            self.save()
            exit(200)

