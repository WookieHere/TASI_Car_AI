from random import Random, randrange, randint
from math import sin

class Neural_Network:
    """Every point has a radian and distance"""
    """Those lead into a hidden layer, which output to the possible commands"""
    def __init__(self, default_function = "Linear"):
        self.default_function = default_function
        self.groups = []
        self.temp_group = []

    def addGroup(self, name):
        self.groups.append(name)
        exec_string = "self.group_"+name+" = []"
        try:
            exec(exec_string)
        except (NameError):
            print("ERROR: Invalid Neural Group Name")

    def addNode(self, group_name):
        if group_name in self.groups:
            new_node = Network_Node()
            exec_string = "self.group_"+group_name+".append(new_node)"
            exec(exec_string)
            return new_node
        else:
            print("ERROR: Invalid Group Name")

    def connectNodes(self, node_a, node_b, function_override = None):
        """Nodes should never be in the same group"""
        if function_override == None:
            node_a.connect(node_b, self.default_function)
        else:
            node_a.connect(node_b, function_override)

    def Input(self, input, group_name):
        if "Input" in group_name and group_name in self.groups:
            i = 0
            for obj in input:
                node_list = self.getGroup(group_name)
                node_list[i].update_input(obj)
                i += 1

    def pulse(self):
        for group in self.groups:
            if "Input" in group:
                node_list = self.getGroup(group)
                for node in node_list:
                    node.evaluate()

        for group in self.groups:
            if "1" in group:
                node_list = self.getGroup(group)
                for node in node_list:
                    node.evaluate()

        for group in self.groups:
            if "2" in group:
                node_list = self.getGroup(group)
                for node in node_list:
                    node.evaluate()

        for group in self.groups:
            if "Output" in group:
                node_list = self.getGroup(group)
                for node in node_list:
                    node.evaluate()
        #all inputs are eval'd

    def getGroup(self, group_name):
        if group_name in self.groups:
            exec_string = "self.temp_group = self.group_" + group_name
            exec(exec_string)
        return self.temp_group



    def pullOutput(self):
        for group in self.groups:
            if "Output" in group:
                node_group = self.getGroup(group)
                if node_group != []:
                    temp = max(node_group);
                    return node_group.index(temp)
                else:
                    print("ERROR: No Outputs in Neural Network")
                    return 0




class Network_Node:
    def __init__(self):
        self.input = 0
        self.connections = []
        self.functions = []


    def update_input(self, new_val):
        self.input = new_val

    def connect(self, node, function_type = None):
        self.connections.append(node)
        self.functions.append(FunctionHelper(function_type))

    def evaluate(self):
        for i in range(0, len(self.functions)):
            self.connections[i].update_input(self.functions[i].calculate_output(self.input))
            #That calculates the output, and sends it to the next node

class FunctionHelper:
    """This class is meant to be a helper class for doing math in nodes"""
    def __init__(self, equation_type = None, learning_rate = .1):
        """More can be added later"""
        self.equ_types = ["Linear", "Sin", "Gaussian"]
        self.rand_handler = Random()
        self.leaning_rate = learning_rate
        self.equation = None
        self.constants = []
        self.function = None
        self.output = 0

        if equation_type in self.equ_types:
            self.equation = equation_type
            self.initialize_equation()
        else:
            self.equation = None

    def initialize_equation(self):
        if self.equation == None:
            print("Error: Abstract equation made it to initialization")
        else:
            if self.equation == "Constant":
                self.constants.append(1)
                self.function = "self.output = self.constants[0]*input"
            elif self.equation == "Linear":
                self.constants.append(1)
                self.constants.append(1)
                self.function = "self.output = self.constants[0]*input + self.constants[1]"
                #those represent sigma and epsilon
                #in y = mx + b respectively
            elif self.equation == "Sin":
                self.constants.append(1)
                self.constants.append(1)
                self.function = "self.output = sin(self.constants[0]*input + self.constants[1])"
                #y = sin(Ax + h)

            elif self.equation == "Gaussion":
                self.constants.append(1)
                self.constants.append(1)
                self.function = "print('Guassion functions have not been implemented yet...')"
                #P(mu, sigma) = <some stuff I don't remember right now>

        """To-do, make a custom equation initializer"""

    def calculate_output(self, input, learn = 1):
        try:
            exec(self.function, input)
            if learn:
                self.learn()
            return self.output
        except (TypeError):
            print("ERROR: Attempted to Evaluate Abstract Function")

    def learn(self, mutation_rate = .25, anneal_rate = .05, rand_resolution = 100):
        const_len = len(self.constants)
        for var in self.constants:
            rand_sel = self.rand_handler.randint(0, const_len * rand_resolution)
            if rand_sel > const_len * rand_resolution * mutation_rate:
                # add or subtract learning rate
                self.mutate(var)
            if rand_sel > const_len * rand_resolution * anneal_rate:
                self.anneal(var)

    def mutate(self, var):
        """This is an abstract mutate for testing"""
        var += self.leaning_rate * pow(-1, self.rand_handler.randint(0, 1))

    def anneal(self, var):
        var = self.rand_handler.randint(-1000, 1000)