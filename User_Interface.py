import array

class UserInterface:
    def __init__(self, Graphics):
        self.GH = Graphics
        self.valid_keys = ["w", "a", "s", "d", "p"]
        self.funcDict = {
            0: "self.changeSpeed(1)",
            1: "self.changeDir(1)",
            2: "self.changeSpeed(-1)",
            3: "self.changeDir(-1)",
            4: "end"
        }


    def checkInput(self):
        keypressed = self.GH.window.checkKey()
        if keypressed != "":
            return self.valid_keys.index(keypressed)
        else:
            return 4

    def processInput(self):
        self.GH.addToEvents(self.funcDict[self.checkInput()])

