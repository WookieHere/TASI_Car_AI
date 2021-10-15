import Frame_Control
import User_Interface
import Field_Interface
import Graphics_Handler
import Lines_and_Dist

class Messager:
    def __init__(self, UserClass, frameRate = .0125):
        self.Frame_Control = Frame_Control.TimerInterrupt(frameRate)  # 60 fps
        self.Field_Interface = Field_Interface.Field_Interface()
        self.Graphics = Graphics_Handler.GHandler()
        self.Input = UserClass
        self.Input.connectMessager(self)
        self.InputCmdList = []
        self.Mode = "Run"
        self.possModes = ["Run", "MapEdit", "Pause"]
        self.mapFile = None
        self.mapFileBuffer = []
        self.Lidar_Pointcloud = []
        self.mapFile = open("Maps.txt", "r")
        #Input can be overriden as an arguement

    def run(self):
        if self.Input.type == "User":
            while True:
                self.Frame_Control.updateFrame(self.Input)
                if self.Mode == "Run":
                    pause_flag = 0
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
                    if pause_flag == 0:
                        self.Graphics.window.setBackground("orange")
                        self.flashLidar(1)
                        if self.Field_Interface.checkCollision():
                            print("Collison Detected!")
                    self.execCommands()
                    pause_flag = 1

                self.Frame_Control.waitForFrame()
        elif self.Input.type == "AI":
            self.Graphics.window.setBackground("white")
            self.flashLidar()
            self.Input.update_sensors(self.Lidar_Pointcloud)
            self.Input.Init()
            while True:
                self.Frame_Control.updateFrame(self.Input)
                self.getCommandList()
                self.execCommands()
                self.Frame_Control.waitForFrame()

    def createMap(self):

        self.Graphics.window.setBackground("yellow")
        self.getMouse()  # this is a loop that runs until exit command is sent
        self.drawMap()


    def getCommandList(self):
        self.InputCmdList = self.Input.pullInput()

    def execCommands(self):
        for x in self.InputCmdList:
            try:
                if "self.changeMode" in x:
                    exec(x)
                elif "addObject(Wall" in x:
                    self.Field_Interface.addWall(x) #this adds a wall to the field interface
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
        self.mapFile = open("Maps.txt", "w")
        print("Input new map name:")
        new_name = input()
        self.mapFile.write(new_name +":\n")
        for x in self.mapFileBuffer:
            self.mapFile.write(x + "\n")
        self.mapFile = open("Maps.txt", "r") #set it back to reading mode

    def loadMap(self, name = None):
        self.mapFile = open("Maps.txt", "r")
        if name == None:
            print("Input map name:")
            name = input()
        line_read = self.mapFile.readline()
        while name not in line_read:
            line_read = self.mapFile.readline()
        while line_read != "\n" and line_read != "":
            line_read = self.mapFile.readline()
            self.mapFileBuffer.append(line_read)
        self.drawMap()

    def drawMap(self):
        self.InputCmdList = self.mapFileBuffer
        self.execCommands()

    def flashLidar(self, draw = 0):
        try:
            self.Lidar_Pointcloud = self.Field_Interface.getPointCloud(self.Graphics.getUserObjects()[0].getPos())
            if draw:
                self.Graphics.drawPointCloud(self.Lidar_Pointcloud)
        except (IndexError):
            pass
        return self.Lidar_Pointcloud