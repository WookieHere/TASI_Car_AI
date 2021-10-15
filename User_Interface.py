from Player_Interface import Player_Interface
import array
import Messager_Facade

class UserInterface(Player_Interface):
    def __init__(self):
        self.type = "User"
        self.to_create = "Wall"
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

    def connectMessager(self, Messager):
        self.Msgr = Messager


    def processInput(self):
        self.cmdList.append(self.funcDict[self.checkInput()])

    def pullInput(self):
        return self.cmdList

    def createCar(self, point):
        new_str = "self.addUserObject(Car(Point(" + str(point.x) + "," + str(point.y) + ")))"
        #self.cmdList.append(new_str)
        return new_str

