
from Handlers import *



class GHandler(Handler):
    def __init__(self, xsize = 1000, ysize = 1000):
        super().__init__()
        self.window = GraphWin('Car_AI', xsize, ysize)
        self.fit_text = Text(Point(100, 20), "Prev Fitness: ")
        self.fit_text.setSize(12)
        self.fit_text.draw(self.window)
        self.best_fit_text = Text(Point(100, 40), "Prev Fitness: ")
        self.best_fit_text.setSize(12)
        self.best_fit_text.draw(self.window)
        self.func_dict = {
            "p" : "Pause",
            "s" : "Save",
            "l" : "Load"
        }
        try:
            super().load(self.save_file)
            print("Network leaded from save file")
        except:
            pass
        """that array will be filled later with things to draw etc."""

    def setText(self, string, string2):
        self.fit_text.setText(string)
        self.best_fit_text.setText(string2)

    def addObject(self, object):
        """object is a string of the init call"""
        super().addObject(object)
        self.Objects[len(self.Objects) - 1].draw(self.window)   #this draws the newly placed object

    def addUserObject(self, object):
        """object is a string of the init call"""
        super().addUserObject(object)
        self.UserObjects[len(self.UserObjects) - 1].draw(self.window)  # this draws the newly placed object

    def drawPointCloud(self, pointcloud):
        for pt in pointcloud.points:
            temp = Circle(Point(pt.x, pt.y), 5)
            temp.setFill('blue')
            temp.draw(self.window)

    def checkInput(self):
        try:
            return self.func_dict[self.window.checkKey()]
        except:
            return None
