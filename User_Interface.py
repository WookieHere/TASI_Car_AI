import array
import Messager_Facade

class UserInterface:
    def __init__(self, Messager):
        self.Type = "User"
        self.to_create = "Wall"
        self.Msgr = Messager
        self.GH = Messager.Graphics
        self.valid_keys = ["w", "a", "s", "d", "o", "p", "r"]
        self.cmdList = []
        self.funcDict = {
            0: "self.changeSpeed(1)",
            1: "self.changeDir(1)",
            2: "self.changeSpeed(-1)",
            3: "self.changeDir(-1)",
            4: "self.changeMode('MapEdit')",
            5: "self.changeMode('Pause')",
            6: "self.changeMode('Run')",
            7: "end"
        }


    def checkInput(self):
        keypressed = self.GH.window.checkKey()
        if keypressed != "":
            print(keypressed)
            try:
                return self.valid_keys.index(keypressed)
            except (ValueError):
                print("Warning: Invalid Key Pressed")
                return len(self.funcDict) - 1  # should return "end"
        else:
            return len(self.funcDict) - 1 #should return "end"

    def checkMouseInput(self):
        key = self.GH.window.checkKey()
        mousePoint = self.GH.window.checkMouse()

        if  key == "e":
            return "exit"
        elif key == "c":
            self.to_create = "Car"
        elif key == "w":
            self.to_create = "Wall"

        if self.to_create == "Car" and mousePoint != None:
            return "makeCar", mousePoint
        elif self.to_create == "Wall" and mousePoint != None:
            return "makeWall", mousePoint
        else:
            return "None"

    def processInput(self):
        self.cmdList.append(self.funcDict[self.checkInput()])

    def pullInput(self):
        return self.cmdList

    def createCar(self, point):
        new_str = "self.addUserObject(Car(Point(" + str(point.x) + "," + str(point.y) + ")))"
        #self.cmdList.append(new_str)
        return new_str

