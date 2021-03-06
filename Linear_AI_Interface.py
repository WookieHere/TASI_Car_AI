from Player_Interface import Player_Interface
import Neural_Network

class AI_Interface(Player_Interface):
    def __init__(self, Messager = None):
        super().__init__(Messager)
        self.type = "AI"
        self.to_create = "Wall"
        self.input_cloud = []
        self.car_speed = 0
        self.car_turnRate = 0
        self.cur_fitness = 0
        self.best_fitness = -999999
        self.Network = Neural_Network.Neural_Network("Linear", 10, 5)
        self.bestNetwork = None
        self.InitNodeGroups()
        self.funcDict = {
            0: "self.changeSpeed(1)",
            1: "self.changeDir(1)",
            2: "self.changeSpeed(-1)",
            3: "self.changeDir(-1)",
            4: "pass"
        }

    def pullNetwork(self):
        return self.Network.best_network

    def setCarParams(self, speed = 0, car_turnRate = 0):
        self.car_speed = speed
        self.car_turnRate = car_turnRate

    def Init(self):
        self.InitNodeGroups()
        self.InitNodes()
        self.Network.learning = 1
        self.Network.updateConfig()
        #self.Network.manualControl()

    def InitNodeGroups(self):
        self.Network.addGroup("Input_Points")
        self.Network.addGroup("Point_Hidden_1")
        self.Network.addGroup("Point_Hidden_2")
        self.Network.addGroup("Input_Car_Parameters")
        self.Network.addGroup("Car_Param_Hidden_2")
        self.Network.addGroup("Output")

    def InitNodes(self):
        """Initialize all nodes in the network (does nto handle input)"""
        car_turnRate = self.Network.addNode("Input_Car_Parameters")
        car_speed = self.Network.addNode("Input_Car_Parameters")
        for point in range(0, self.input_cloud.resolution):
            pt = self.Network.addNode("Input_Points")
            pt_dist = self.Network.addNode("Point_Hidden_1")
            pt_H = self.Network.addNode("Point_Hidden_2")
            self.Network.connectNodes(pt, pt_dist, "Custom", "self.output = input.dist")
            self.Network.connectNodes(pt_dist, pt_H)
            #self.Network.connectNodes(car_speed, pt_H, "Custom", "self.output = input")
            #self.Network.connectNodes(car_turnRate, pt_H, "Custom", "self.output = input")

        for node in self.Network.getGroup("Input_Car_Parameters"):
            new_node = self.Network.addNode("Car_Param_Hidden_2")
            self.Network.connectNodes(node, new_node, "Custom", "self.output = input")


        for output in self.funcDict:
            out = self.Network.addNode("Output")
            for node in self.Network.getGroup("Point_Hidden_2"):
                self.Network.connectNodes(node, out)
            for node in self.Network.getGroup("Car_Param_Hidden_2"):
                self.Network.connectNodes(node, out)
            """
            for node in self.Network.getGroup("Input_Car_Parameters"):
                self.Network.connectNodes(node, out)
            """

    def setFitness(self, fitness):
        self.cur_fitness = fitness
        if self.cur_fitness > self.best_fitness:
            self.best_fitness = self.cur_fitness
            self.bestNetwork = self.Network.best_network
        self.Network.setFitness(self.cur_fitness)

    def processInput(self):
        """This is the Neural Network function"""
        """This particular AI has a placeholder linear Network"""
        """Obeys y = mx+b style format (replace m with alpha and b with epsilon for lookup)"""
        self.Network.inputPointCloud(self.input_cloud.points, "Input_Points")
        params = [self.car_speed, self.car_turnRate]
        self.Network.inputCarParams(params, "Input_Car_Parameters")
        self.Network.pulse()
        output_index = self.Network.pullOutput()
        self.cmdList.append(self.funcDict[output_index])

    def pullInput(self):
        return self.cmdList

    def updateIteration(self):
        self.Network.pulse(1, "Batch")
        if self.Network.checkProgress() == "Reset":
            self.Network = self.Network.best_network
            self.Network.best_network = self.Network.saveNetwork()
            self.Network.learn_count = 0

    def createCar(self, point):
        new_str = "self.addUserObject(Car(Point(" + str(point.x) + "," + str(point.y) + ")))"
        # self.cmdList.append(new_str)
        return new_str

    def update_sensors(self, new_cloud):
        self.input_cloud = new_cloud