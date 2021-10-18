from random import Random, randrange, randint
from math import sin, cos

class Neural_Network:
    """Every point has a radian and distance"""
    """Those lead into a hidden layer, which output to the possible commands"""
    def __init__(self, default_function = "Linear"):
        self.default_function = default_function
        self.groups = []
        self.temp_group = []
        self.fitness = 0
        self.learning = 0

    def setFitness(self, fitness):
        self.fitness = fitness
        for group in self.groups:
            node_group = self.getGroup(group)
            for node in node_group:
                node.fitness = self.fitness


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
            new_node = Network_Node()
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
                    return temp
                else:
                    print("ERROR: No Outputs in Neural Network")
                    return 0

    def getMaxIndex(self, node_group):
        max = -1000000
        max_index = 0
        for node in node_group:
            if node.input > max:
                max = node.input
                max_index = node_group.index(node)
        return max_index

    def flushNetwork(self):
        for group in self.groups:
            node_list = self.getGroup(group)
            for node in node_list:
                node.input = 0



class Network_Node:
    def __init__(self, learning_rate = 1):
        self.input = 0
        self.learning_rate = learning_rate
        self.connections = []
        self.functions = []
        self.fitness = 0


    def update_input(self, new_val):
        try:
            self.input += new_val
        except (TypeError):
            self.input = new_val

    def connect(self, node, function_type = None, custom_func_string = None):
        self.connections.append(node)
        self.functions.append(FunctionHelper(function_type, self.learning_rate, custom_func_string))

    def evaluate(self, learning = 0, mode = "Stochastic"):
        for i in range(0, len(self.functions)):
            self.connections[i].update_input(self.functions[i].calculate_output(self.input))
            if learning and mode == "Stochastic":
                self.functions[i].learn(self.fitness)
            elif learning and mode == "Batch":
                self.functions[i].batchLearn(self.fitness)
            #That calculates the output, and sends it to the next node

    def printFunctions(self):
        for k in range(0, len(self.connections)):
            self.functions[k].printFunction()

class FunctionHelper:
    """This class is meant to be a helper class for doing math in nodes"""
    def __init__(self, equation_type = None, learning_rate = 50, equ_string = ""):
        """More can be added later"""
        self.equ_types = ["Linear", "Sin", "Gaussian", "Custom"]
        self.rand_handler = Random()
        self.leaning_rate = learning_rate
        self.equation = None
        self.best_constants = []
        self.best_fitness = 0
        self.iterations_since_updated = []
        self.constants = []
        self.fitnesses = []
        self.selection_bool = []
        self.function = None

        self.input = 0
        self.output = 0

        if equation_type in self.equ_types and equation_type != "Custom":
            self.equation = equation_type
            self.initialize_equation()
        elif equation_type == "Custom":
            self.equation = equation_type
            self.function = equ_string
        else:
            self.equation = None


    def printFunction(self, outfile = None):
        if outfile != None:
            if self.equation == "Constant":
                outfile.write("output = " + str(self.constants[0]) + " * x\n")
            elif self.equation == "Linear":
                outfile.write("output = " + str(self.constants[0]) + " * x + " + str(self.constants[1]) + "\n")
                # those represent sigma and epsilon
                # in y = mx + b respectively
            elif self.equation == "Sin":
                outfile.write("output = sin(" + str(self.constants[0]) + " * x + " + str(self.constants[1]) + ")\n")
                # y = sin(Ax + h)
            elif self.equation == "Gaussion":
                print("Guassion functions have not been implemented yet...")

            elif self.equation == "Custom":
                print(self.function)
        try:
            if self.equation == "Constant":
                print("output = " + str(self.constants[0]) + " * x")
            elif self.equation == "Linear":
                print("output = " + str(self.constants[0]) + " * x + " + str(self.constants[1]))
                # those represent sigma and epsilon
                # in y = mx + b respectively
            elif self.equation == "Sin":
                print("output = sin(" + str(self.constants[0]) + " * x + " + str(self.constants[1]) + ")")
                # y = sin(Ax + h)
            elif self.equation == "Gaussion":
                print("Guassion functions have not been implemented yet...")

            elif self.equation == "Custom":
                print(self.function)
            else:
                print("ERROR: Equation Type not Detected in printFunctions()")

        except (IndexError):
            #print("Warning: No constants in " + self.equation + " function")
            pass

    def initialize_equation(self):
        if self.equation == None:
            print("Error: Abstract equation made it to initialization")
        else:
            if self.equation == "Constant":
                self.addConstant()
                self.function = "self.output = self.constants[0]*self.input"
            elif self.equation == "Linear":
                self.addConstant()
                self.addConstant()
                self.function = "self.output = self.constants[0]*self.input + self.constants[1]"
                #those represent sigma and epsilon
                #in y = mx + b respectively
            elif self.equation == "Sin":
                self.addConstant()
                self.addConstant()
                self.function = "self.output = sin(self.constants[0]*self.input + self.constants[1])"
                #y = sin(Ax + h)

            elif self.equation == "Gaussion":
                self.addConstant()
                self.addConstant()
                self.function = "print('Guassion functions have not been implemented yet...')"
                #P(mu, sigma) = <some stuff I don't remember right now>
        """To-do, make a custom equation initializer? (see init function)"""

    def addConstant(self, value = 0):
        self.constants.append(value)
        self.fitnesses.append(-999999)
        self.iterations_since_updated.append(0)
        self.best_constants.append(0)
        self.selection_bool.append(0)


    def calculate_output(self, input):
        self.input = input
        try:
            exec(self.function)
            return self.output
        except (TypeError):
            print("ERROR: Attempted to Evaluate Abstract Function")

    def learn(self, fitness, batch_length = 5, mutation_rate = .10, anneal_rate = .01, rand_resolution = 100):
        const_len = len(self.constants)
        #This saves the best constants so far
        for k in range(0, len(self.fitnesses)):
            if fitness > self.fitnesses[k]:
                self.fitnesses[k] = fitness
                self.best_constants[k] = self.constants[k]
                self.iterations_since_updated[k] = 0

        for k in range(0, len(self.iterations_since_updated)):
            if self.iterations_since_updated[k] > batch_length:
                self.constants[k] = self.best_constants[k]
                self.iterations_since_updated[k] = 0
            else:
                self.iterations_since_updated[k] += 1

        for var_index in range(0, len(self.constants)):
            rand_sel = self.rand_handler.randint(0, const_len * rand_resolution)
            if rand_sel < const_len * rand_resolution * mutation_rate:
                # add or subtract learning rate
                self.mutate(var_index)
            if rand_sel < const_len * rand_resolution * anneal_rate:
                self.anneal(var_index)

    def batchLearn(self, fitness, batch_length = 10, mutation_rate = .50, anneal_rate = .00, rand_resolution = 100):
        const_len = len(self.constants)
        # This saves the best constants so far
        if fitness > self.best_fitness:
            self.best_fitness = fitness

        for k in range(0, len(self.fitnesses)):
            if fitness > self.fitnesses[k] and self.selection_bool[k] != 0:
                self.fitnesses[k] = fitness
                self.setBestConstants(self.constants[k], k)
                self.iterations_since_updated[k] = 0

        for k in range(0, len(self.iterations_since_updated)):
            if self.iterations_since_updated[k] > batch_length:
                self.setConstant(k, self.best_constants[k])
                self.iterations_since_updated[k] = 0
                self.selectConstants()
            else:
                self.iterations_since_updated[k] += 1

        for var_index in range(0, len(self.constants)):
            rand_sel = self.rand_handler.randint(0, const_len * rand_resolution)
            if self.selection_bool[var_index] == 1:
                self.printFunction()
                if rand_sel < const_len * rand_resolution * mutation_rate:
                    # add or subtract learning rate
                    self.mutate(var_index)
                if rand_sel < const_len * rand_resolution * anneal_rate:
                    self.anneal(var_index)

    def mutate(self, var_index):
        """This is an abstract mutate for testing"""
        self.constants[var_index] += self.leaning_rate * pow(-1, self.rand_handler.randint(0, 1))

    def anneal(self, var_index):
        self.constants[var_index] = self.rand_handler.randint(-100, 100)

    def setConstant(self, index, value):
        self.constants[index] = value

    def setBestConstants(self, values, index = None):
        if index != None:
            self.best_constants[index] = values
        else:
            self.best_constants = values

    def selectConstants(self, chance = 2):
        for k in range(0, len(self.constants)):
            self.selection_bool[k] = 0
            if self.rand_handler.randint(0, 100) < chance:
                self.selection_bool[k] = 1