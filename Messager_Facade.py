import Frame_Control
import User_Interface
import Field_Interface
import Graphics_Handler

class Messager:
    def __init__(self, UsrCmd = None, frameRate = .0125):
        self.Frame_Control = Frame_Control.TimerInterrupt(frameRate)  # 60 fps
        self.Field_Interface = Field_Interface.Field_Interface()
        self.Graphics = Graphics_Handler.GHandler()
        self.Input = User_Interface.UserInterface(self)
        self.InputCmdList = []
        self.Mode = "Run"
        self.possModes = ["Run", "MapEdit", "Pause"]
        self.mapFile = None
        self.mapFileBuffer = []
        #Input can be overriden as an arguement
        try:
            if UsrCmd.Type != "User":
                self.Input = UsrCmd
        except (TypeError, AttributeError):
            pass


        while True:
            self.Frame_Control.updateFrame(self.Input)
            if self.Mode == "Run":
                self.Graphics.window.setBackground("white")
                self.getCommandList()
                self.execCommands()
            elif self.Mode == "MapEdit":
                self.mapFile = open("Maps.txt", "a+")
                self.Graphics.window.setBackground("yellow")
                self.getMouse() #this is a loop that runs until exit command is sent
                self.InputCmdList = self.mapFileBuffer
                self.execCommands()
                #self.saveMap()
                self.Mode = "Run"
            else:
                #assumed mode is "Pause"
                self.Graphics.window.setBackground("orange")
                self.execCommands()

            self.Frame_Control.waitForFrame()

    def getCommandList(self):
        self.InputCmdList = self.Input.pullInput()

    def execCommands(self):
        for x in self.InputCmdList:
            try:
                if "self.changeMode" in x:
                    exec(x)
            except (AttributeError, NameError):
                pass
        """that looks for commands to the messager, then passes the rest off to the field handler"""
        self.Field_Interface.modify(self.InputCmdList)
        self.Graphics.setEvents(self.InputCmdList)
        self.Graphics.popAllEvents()

    def changeMode(self, newMode):
        if self.possModes.__contains__(newMode):
            self.Mode = newMode

    def getMouse(self):
        newCommand = self.Frame_Control.getMouse(self.Input)
        while newCommand != -1:
            self.mapFileBuffer.append(newCommand)
            newCommand = self.Frame_Control.getMouse(self.Input)

    def saveMap(self):
        print("Input new map name:")
        new_name = input()
        self.mapFile.write(new_name)
        for x in self.mapFileBuffer:
            self.mapFile.write(x)

    def loadMap(self):
        print("Input new map name:")
        new_name = input()
        """This is a to-do"""