from random import Random, randrange, randint

class FunctionHelper:
    """This class is meant to be a helper class for doing math in nodes"""
    def __init__(self, equation_type = None, learning_rate = 50, equ_string = ""):
        """More can be added later"""
        self.equ_types = ["Linear", "Sin", "Gaussian", "Custom"]
        self.rand_handler = Random()
        self.leaning_rate = learning_rate
        self.equation = None
        self.iterations_since_updated = 0
        self.constants = []
        self.selection_bool = []
        self.function = None
        self.input = 0
        self.output = 0
        self.batch_length = 20

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
                outfile.write(self.function + "\n")
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
        self.selection_bool.append(0)


    def calculate_output(self, input):
        self.input = input
        try:
            exec(self.function)
            return self.output
        except (TypeError):
            print("ERROR: Attempted to Evaluate Abstract Function")

    def stochasticLearn(self, batch_length = 10, mutation_rate = .10, anneal_rate = .01, rand_resolution = 100):
        const_len = len(self.constants)
        #This saves the best constants so far

        for var_index in range(0, len(self.constants)):
            rand_sel = self.rand_handler.randint(0, const_len * rand_resolution)
            self.printFunction()
            if rand_sel < const_len * rand_resolution * mutation_rate:
                # add or subtract learning rate
                self.mutate(var_index)
            if rand_sel < const_len * rand_resolution * anneal_rate:
                self.anneal(var_index)

    def batchLearn(self, batch_length = 10, mutation_rate = .50, anneal_rate = .00, rand_resolution = 100):
        const_len = len(self.constants)

        if self.iterations_since_updated > batch_length:
            self.iterations_since_updated = 0
            self.selectConstants()
        else:
            self.iterations_since_updated += 1

        for var_index in range(0, const_len):
            rand_sel = self.rand_handler.randint(0, const_len * rand_resolution)
            if self.selection_bool[var_index] == 1:
                self.printFunction()
                if rand_sel < const_len * rand_resolution * mutation_rate:
                    # add or subtract learning rate
                    self.mutate(var_index)
                if rand_sel < const_len * rand_resolution * anneal_rate:
                    self.anneal(var_index)

    def detLearn(self, batch_length = 20):
        const_len = len(self.constants)

        if self.iterations_since_updated > batch_length:
            self.iterations_since_updated = 0
            self.selectConstants()
            for var_index in range(0, const_len):
                # rand_sel = self.rand_handler.randint(0, const_len * rand_resolution)
                if self.selection_bool[var_index] == 1:
                    self.constants[var_index] -= (.5 * batch_length)
        else:
            self.iterations_since_updated += 1

        for var_index in range(0, const_len):
            #rand_sel = self.rand_handler.randint(0, const_len * rand_resolution)
            if self.selection_bool[var_index] == 1:
                self.printFunction()
                self.constants[var_index] += 1


    def mutate(self, var_index):
        """This is an abstract mutate for testing"""
        self.constants[var_index] += self.rand_handler.randint(-self.leaning_rate, self.leaning_rate)

    def anneal(self, var_index):
        self.constants[var_index] = self.rand_handler.randint(-100, 100)

    def setConstant(self, value, index):
        self.constants[index] = value

    def selectConstants(self, chance = 5):
        for k in range(0, len(self.constants)):
            self.selection_bool[k] = 0
            if self.rand_handler.randint(0, 100) < chance:
                self.selection_bool[k] = 1

"""
    def setBestConstants(self, values, index = None):
        if index != None:
            self.best_constants[index] = values
        else:
            self.best_constants = values
"""
