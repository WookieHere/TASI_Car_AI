import copy
from Learning_Functions import *

from math import sin, cos

class Neural_Network:
    """Every point has a radian and distance"""
    """Those lead into a hidden layer, which output to the possible commands"""
    def __init__(self, default_function = "Linear", learn_rate = 10, default_batchlength = 10):
        self.default_function = default_function
        self.groups = []
        self.temp_group = []
        self.learn_rate = learn_rate
        self.batch_len = default_batchlength
        self.learn_count = 0
        self.fitness = 0
        self.best_fitness = -9999999
        self.batch_best_fitness = -9999999
        self.best_network = None
        self.learning = 1

    def checkProgress(self):
        if self.learn_count > self.batch_len:
            if self.batch_best_fitness < self.best_fitness:
                return "Reset"
            else:
                self.batch_best_fitness = -9999999
                self.learn_count = 0
        else:
            self.learn_count += 1

    def setFitness(self, fitness):
        self.fitness = fitness
        if self.fitness > self.batch_best_fitness:
            self.batch_best_fitness = self.fitness
        if self.fitness > self.best_fitness:
            self.best_fitness = fitness
            self.best_network = self.saveNetwork()
            for group in self.groups:
                node_group = self.getGroup(group)
                for node in node_group:
                    node.fitness = self.fitness

    def saveNetwork(self):
        return copy.deepcopy(self)

    def updateConfig(self):
        for group in self.groups:
            node_group = self.getGroup(group)
            for node in node_group:
                node.fitness = self.fitness
                node.learning = self.learning

    def addGroup(self, name):
        if name not in self.groups:
            self.groups.append(name)
            exec_string = "self.group_"+name+" = []"
            try:
                exec(exec_string)
            except (NameError):
                print("ERROR: Invalid Neural Group Name")

    def addNode(self, group_name):
        if group_name in self.groups:
            new_node = Network_Node(self.learn_rate, self.batch_len)
            exec_string = "self.group_"+group_name+".append(new_node)"
            exec(exec_string)
            return new_node
        else:
            print("ERROR: Invalid Group Name")

    def connectNodes(self, node_a, node_b, function_override = None, custom_func_string = None):
        """Nodes should never be in the same group"""
        if function_override == None:
            node_a.connect(node_b, self.default_function)
        else:
            node_a.connect(node_b, function_override, custom_func_string)

    def inputPointCloud(self, input, group_name):
        if "Input" in group_name and group_name in self.groups:
            i = 0
            node_list = self.getGroup(group_name)
            radian_list = []
            for obj in input:
                try:
                    if obj.radian not in radian_list:
                        node_list[i].update_input(obj)
                        radian_list.append(obj.radian)
                        i += 1
                except (IndexError):
                    print("WARNING: 2xResolution != Points in Input_Cloud")

    def inputCarParams(self, input, group_name):
        if "Input" in group_name and group_name in self.groups:
            i = 0
            node_list = self.getGroup(group_name)
            for obj in input:
                node_list[i].update_input(obj)
                i += 1


    def pulse(self, learning_bool = 0, mode = "Stochastic"):
        if learning_bool != self.learning:
            learning_bool = 0
        for group in self.groups:
            if "Input" in group:
                node_list = self.getGroup(group)
                for node in node_list:
                    node.evaluate(learning_bool, mode)

        for group in self.groups:
            if "1" in group:
                node_list = self.getGroup(group)
                for node in node_list:
                    node.evaluate(learning_bool, mode)

        for group in self.groups:
            if "2" in group:
                node_list = self.getGroup(group)
                for node in node_list:
                    node.evaluate(learning_bool, mode)

        for group in self.groups:
            if "Output" in group:
                node_list = self.getGroup(group)
                for node in node_list:
                    node.evaluate(learning_bool, mode)
        #all inputs are eval'd

    def getGroup(self, group_name):
        if group_name in self.groups:
            exec_string = "self.temp_group = self.group_" + group_name
            exec(exec_string)
        return self.temp_group

    def printConnections(self):
        for group in self.groups:
            node_group = self.getGroup(group)
            for node_num in range(0, len(node_group)):
                node_group[node_num].printFunctions()

    def manualControl(self):
        sel_group = []
        while "exit" not in sel_group:
            for group in self.groups:
                print(group)
                node_list = self.getGroup(group)
                i = 0
                for node in node_list:
                    print(str(i) + ":")
                    i += 1
                    j = 0
                    for f in node.functions:
                        print("   " + str(j) +":", end = "")
                        f.printFunction()
                        j += 1

            try:
                node_sel = input("Enter a node: (Format is <group> <node> <connection>) \n")
                sel_group = node_sel.split(" ")
                sel_group[1] = int(sel_group[1])
                sel_group[2] = int(sel_group[2])

                if sel_group[0] in self.groups:
                    node_list = self.getGroup(sel_group[0])
                    node = node_list[sel_group[1]]
                    func = node.functions[sel_group[2]]
                    func.printFunction()
                    print("What would you like to edit? (<index> <value>)")
                    func_in = input("")
                    sel_group = func_in.split(" ")
                    func.setConstant(int(sel_group[0]), int(sel_group[1]))

                    print("New function:")
                    func.printFunction()
                    print("Done? (y/n)")
                    sel_group = input("")
                    if sel_group == "y":
                        print("Save? (y/n)")
                        save_bool = input("")
                        if save_bool == "y":
                            self.exportNetwork()
                        sel_group = "exit"
                        break
            except (IndexError, ValueError):
                print("Invalid Selection")

    def exportNetwork(self):
        out = open("Network.txt", "w")
        for group in self.groups:
            out.write(group + "\n")
            node_list = self.getGroup(group)
            i = 0
            for node in node_list:
                out.write(str(i) + ":\n")
                i += 1
                j = 0
                for f in node.functions:
                    out.write("   " + str(j) + ":")
                    f.printFunction(out)
                    j += 1

    def pullOutput(self):
        for group in self.groups:
            if "Output" in group:
                node_group = self.getGroup(group)
                if node_group != []:
                    temp = self.getMaxIndex(node_group);
                    self.flushNetwork()
                    return temp
                else:
                    print("ERROR: No Outputs in Neural Network")
                    return 0

    def flushNetwork(self):
        for group in self.groups:
            for node in self.getGroup(group):
                #node.input = 0
                try:
                    node.input -= node.input
                    node.output = 0
                except:
                    pass
                for func in node.functions:
                    #func.flush()
                    pass

    def getMaxIndex(self, node_group):
        max = -1000000
        max_index = 0
        for node in node_group:
            if node.input > max:
                max = node.input
                max_index = node_group.index(node)
        return max_index

    """def flushNetwork(self):
        for group in self.groups:
            node_list = self.getGroup(group)
            for node in node_list:
                node.input = 0
    """



class Network_Node:
    def __init__(self, learning_rate = 1, batch_size = 10):
        self.input = 0
        self.learning_rate = learning_rate
        self.connections = []
        self.functions = []
        self.fitness = 0


    def update_input(self, new_val):
        try:
            self.input += new_val #this was formerly =
        except (TypeError):
            self.input = new_val

    def connect(self, node, function_type = None, custom_func_string = None):
        self.connections.append(node)
        self.functions.append(FunctionHelper(function_type, self.learning_rate, custom_func_string))

    def evaluate(self, learning = 0, mode = "Stochastic"):
        for i in range(0, len(self.functions)):
            self.connections[i].update_input(self.functions[i].calculate_output(self.input))
            if learning and mode == "Stochastic":
                self.functions[i].stochasticLearn()
            elif learning and mode == "Batch":
                self.functions[i].batchLearn()
            elif learning and mode == "Deterministic":
                self.functions[i].detLearn()
            #That calculates the output, and sends it to the next node

    def printFunctions(self):
        for k in range(0, len(self.connections)):
            self.functions[k].printFunction()

