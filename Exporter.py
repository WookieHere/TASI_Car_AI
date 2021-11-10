from Neural_Network import *

class Exporter:
    def __init__(self, net):
        self.path = Queue()
        self.Network = net
        self.output_keys = [0, 1, 2, 3, 4]
        self.output_file = open("Network.txt", "w")

    def export(self):
        output_connections = []
        for group in self.Network.groups:
            if "Output" in group:
                temp_group = self.Network.getGroup(group)
                for node in temp_group:
                    output_connections.append(self.getConnectedFunctions(node))
                    """Method is going to be recursively find all connections and evaluate. 
                    you will end up and inputs every time
                    """

    def queueFunctions(self):
        for group in self.Network.groups:
            if "Input" in group:
                temp_group = self.Network.getGroup(group)
                for node in temp_group:
                   self.recursivePrint(node)


    def recursivePrint(self, node):
        i = 0

        for c in node.connections:
            self.path.push(node.functions[i])
            self.recursivePrint(c)
            #node.functions[i].printFunction()
            self.path.popObj(node.functions[i])
            i += 1
        if len(node.connections) == 0:

            self.inlineFuncPrint("Output " + str(self.Network.group_Output.index(node)) + ":", open("Network.txt", "a"))
            # leaf node

    def inlineFuncPrint(self, output_num, outfile = None):
        len_flag = 0
        head_str = output_num
        hold_str = ""
        temp_str = ""
        reverse_queue = self.path.reverseCopy()
        traversal = reverse_queue.first
        while traversal != None:
            if len_flag == 0:
                hold_str += "(" + traversal.data.function.replace("self.output = ", "") + ")"
                len_flag = 1
            elif len(traversal.data.constants) == 2:
                temp_str = "(" + str(traversal.data.constants[0]) + hold_str + "+" + str(traversal.data.constants[1]) + ")"
                hold_str = temp_str
            traversal = traversal.next
        hold_str = head_str + hold_str
        if outfile == None:
            print(hold_str)
        else:
            outfile.write(hold_str + "\n")

    def isConnected(self, node_a, node_b):
        """This function checks to see if node_b is a connection of node_a"""
        if node_b in node_a.connections:
            return True
        else:
            return False

    def getConnectedFunctions(self, target):
        ret_list = []
        for group in self.Network.groups:
            temp_group = self.Network.getGroup(group)
            for node in temp_group:
                if self.isConnected(node, target):
                    ret_list.append(node.functions[node.connections.index(target)]) #returns function by which they are connected
        return  ret_list

class Queue:
    def __init__(self):
        self.len = 0
        self.first = None

    def push(self, obj):
        """pushes obj to front of queue"""
        temp = None
        if self.len > 0:
            temp = self.first
        self.first = Node(obj)
        self.first.next = temp
        self.len += 1

    def popEnd(self):
        """pops from end of queue"""
        temp = self.first
        if self.len == 0:
            pass
        else:
            for i in range(0, self.len - 1):
                temp = temp.next
            del temp.next
            self.len -= 1

    def pop(self):
        """pops from front"""
        self.first = self.first.next
        self.len -= 1

    def popObj(self, obj):
        traversal = self.first.next
        tail = self.first
        if self.first.data == obj:
            self.pop()
        else:
            while traversal != None:
                if traversal.data == obj:
                    tail.next = traversal.next
                    del traversal
                    break
            pass #this is just to leave a breakpoint here

    def reverseCopy(self):
        new_queue = Queue()
        traversal = self.first
        for i in range(0, self.len):
            new_queue.push(traversal.data)
            traversal = traversal.next
        return new_queue

class Node:
    def __init__(self, obj):
        self.data = obj
        self.next = None