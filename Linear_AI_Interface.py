from Player_Interface import Player_Interface
import Neural_Network

class AI_Interface(Player_Interface):
    def __init__(self, Messager = None):
        super().__init__(Messager)
        self.type = "AI"
        self.to_create = "Wall"
        self.input_cloud = []
        self.Network = Neural_Network.Neural_Network("Linear")
        self.InitNodeGroups()
        self.funcDict = {
            0: "self.changeSpeed(1)",
            1: "self.changeDir(1)",
            2: "self.changeSpeed(-1)",
            3: "self.changeDir(-1)"
        }

    def Init(self):
        self.InitNodeGroups()
        self.InitNodes()

    def InitNodeGroups(self):
        self.Network.addGroup("Input_Points")
        self.Network.addGroup("Point_Hidden_1")
        self.Network.addGroup("Point_Hidden_2")
        self.Network.addGroup("Output")

    def InitNodes(self):
        for point in self.input_cloud:
            pt = self.Network.addNode("Input_Points")
            pt_rad = self.Network.addNode("Point_Hidden_1")
            pt_dist = self.Network.addNode("Point_Hidden_1")
            pt_H = self.Network.addNode("Point_Hidden_2")
            self.Network.connectNodes(pt, pt_rad)
            self.Network.connectNodes(pt, pt_dist)
            self.Network.connectNodes(pt_rad, pt_H)
            self.Network.connectNodes(pt_dist, pt_H)

        for output in self.funcDict:
            out = self.Network.addNode("Output")
            for node in self.Network.group_Point_Hidden_2:
                self.Network.connectNodes(node, out)

    def processInput(self):
        """This is the Neural Network function"""
        """This particular AI has a placeholder linear Network"""
        """Obeys y = mx+b style format (replace m with alpha and b with epsilon for lookup)"""
        self.Network.Input(self.input_cloud, "Input_Points")
        self.Network.pulse()
        #output_index = self.Network.pullOutput()

        pass

    def pullInput(self):
        return self.cmdList

    def createCar(self, point):
        new_str = "self.addUserObject(Car(Point(" + str(point.x) + "," + str(point.y) + ")))"
        # self.cmdList.append(new_str)
        return new_str

    def update_sensors(self, new_cloud):
        self.input_cloud = new_cloud


