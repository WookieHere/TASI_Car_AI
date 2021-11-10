import Frame_Control
import User_Interface
import Field_Interface
import Graphics_Handler
import Lines_and_Dist
import copy
import Exporter

test = Exporter.Exporter(None)

class Messager:
    def __init__(self, UserClass, HandlerClass, frameRate = .0125):
        self.Frame_Control = Frame_Control.TimerInterrupt(frameRate)  # 60 fps
        self.Field_Interface = Field_Interface.Field_Interface()
        self.Handler = HandlerClass
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

    def setFrameRate(self, framerate, debugmode = None):
        self.Frame_Control.setFrameRate(framerate, debugmode)

    def run(self):
        if self.Input.type == "User":
            """User Run Loop"""
            self.run_User()

        elif self.Input.type == "AI":
            """This section is for the AI"""
            #self.Handler.window.setBackground("white")
            self.flashLidar()
            self.Input.update_sensors(self.Lidar_Pointcloud)
            self.Input.setCarParams(self.getCarParams("Speed"), self.getCarParams("Dir"))
            self.Input.Init()
            self.Field_Interface.setCheckPoint(self.getCarParams("Pos"))
            self.Field_Interface.Reward_Track.setTrack(self.Handler.getObjects())
            self.Field_Interface.Reward_Track.setCheckPoints()
            self.Field_Interface.Reward_Track.drawCheckpoints(self.Handler)
            #self.Input.Network.manualControl()
            test.Network = self.Input.Network
            test.queueFunctions()
            self.run_AI()


    def run_AI(self):
        while True:
            self.Frame_Control.updateFrame(self.Input)
            self.getCommandList()
            self.execCommands()
            self.flashLidar()
            self.Field_Interface.fitnessUpdate()
            if self.Field_Interface.ruleCheck():
                self.Input.setFitness(self.Field_Interface.fitnessFunc())
                self.Field_Interface.clearFitness()
                self.Input.updateIteration()
                self.Field_Interface.resetCar(self.getCar())
                self.Input.Network.flushNetwork()
                self.Handler.incIterations()

                try:
                    self.Handler.setText("Prev Fitness: " + str(self.Input.cur_fitness), "Best Fitness "+ str(self.Input.best_fitness))
                    input = self.Handler.checkInput()
                    self.processWindowInput(input)
                except (AttributeError):
                    pass
                    #Not a graphical interface
                # self.Input.Network.printConnections()
            self.Input.update_sensors(self.Lidar_Pointcloud)
            self.Input.setCarParams(self.getCarParams("Speed"), self.getCarParams("TurnRate"))
            self.Frame_Control.waitForFrame()

    def run_User(self):
        while True:
            self.Frame_Control.updateFrame(self.Input)
            if self.Mode == "Run":
                pause_flag = 0
                self.Handler.window.setBackground("white")
                self.getCommandList()
                self.execCommands()

            elif self.Mode == "MapEdit":
                self.mapFile = open("Maps.txt", "a+")
                self.Handler.window.setBackground("yellow")
                self.getMouse()  # this is a loop that runs until exit command is sent
                self.InputCmdList = self.mapFileBuffer
                self.execCommands()
                self.Mode = "Run"
            else:
                # assumed mode is "Pause"
                if pause_flag == 0:
                    self.Handler.window.setBackground("orange")
                    self.flashLidar(1)
                    if self.Field_Interface.checkCollision():
                        print("Collison Detected!")
                self.execCommands()
                pause_flag = 1

            self.Frame_Control.waitForFrame()

    def createMap(self):
        self.Handler.window.setBackground("yellow")
        self.getMouse()  # this is a loop that runs until exit command is sent
        self.drawMap()


    def getCommandList(self):
        self.InputCmdList = self.Input.pullInput()

    def processWindowInput(self, str):
        if str == "Pause":
            input("Paused: Press any key to continue")
        elif str == "Save":
            self.Input.Network.best_network.exportNetwork()
            self.Handler.save(self.Input)
        elif str == "Load":
            self.Handler.load(self.Input)

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
        self.Handler.setEvents(self.InputCmdList)
        self.Handler.popAllEvents()

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
        self.InputCmdList = copy.deepcopy(self.mapFileBuffer)
        self.execCommands()

    def flashLidar(self, draw = 0):
        try:
            self.Lidar_Pointcloud = self.Field_Interface.getPointCloud(self.getCarParams("Pos"), self.getCarParams("Dir"))
            if draw:
                self.Handler.drawPointCloud(self.Lidar_Pointcloud)
        except (IndexError):
            pass
        return self.Lidar_Pointcloud

    def getCar(self, index = 0):
        return self.Handler.getUserObjects()[index]

    def getCarParams(self, param_name = None, index = 0):
        car = self.getCar(index)
        if param_name == None or param_name == "All":
            return car.getPos()
            return car.carDirRad
            return car.carSpeed
        elif param_name == "Speed":
            return car.carSpeed
        elif param_name == "Dir":
            return car.carDirRad
        elif param_name == "TurnRate":
            return car.turnRate
        elif param_name == "Pos":
            return car.getPos()
