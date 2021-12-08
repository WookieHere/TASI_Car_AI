

class Player_Interface:
    def __init__(self, Messager = None):
        self.type = "Abstract"
        self.to_create = "Null"
        self.Msgr = Messager
        self.valid_keys = []
        self.cmdList = []
        self.funcDict = []

    def connectMessager(self, Messager):
        self.Msgr = Messager

    def processInput(self):
        pass

    def pullInput(self):
        return self.cmdList

    def createCar(self, point):
        new_str = "self.addUserObject(Car(Point(" + str(point.x) + "," + str(point.y) + ")))"
        #self.cmdList.append(new_str)
        return new_str

    def checkInput(self):
        keypressed = self.Msgr.Handler.window.checkKey()
        if keypressed != "":
            #print(keypressed)
            try:
                return self.valid_keys.index(keypressed)
            except (ValueError):
                print("Warning: Invalid Key Pressed")
                return len(self.funcDict) - 1  # should return "end"
        else:
            return len(self.funcDict) - 1  # should return "end"

    def checkMouseInput(self):
        key = self.Msgr.Handler.window.checkKey()
        mousePoint = self.Msgr.Handler.window.checkMouse()

        if key == "e":
            return "exit"
        elif key == "c":
            self.to_create = "Car"
        elif key == "w":
            self.to_create = "Wall"
        elif key == "d":
            self.Msgr.drawMap()
        elif key == "s":
            self.Msgr.saveMap()
        elif key == "l":
            self.Msgr.loadMap()
        elif key == "r":
            self.to_create = "TrackLine"

        if self.to_create == "Car" and mousePoint != None:
            return "makeCar", mousePoint
        elif self.to_create == "Wall" and mousePoint != None:
            return "makeWall", mousePoint
        elif self.to_create == "TrackLine" and mousePoint != None:
            return "makeTrackLine", mousePoint
        else:
            return "None"

