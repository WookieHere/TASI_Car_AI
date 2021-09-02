from graphics import *
import math
from Object_Handler import *
import Lines_and_Dist

class Car(UserObject):
    def __init__(self):
        super().__init__()
        self.name = "Car"
        self.car = Rectangle(Point(10, 10), Point(50, 50))
        self.car.setFill('yellow')
        self.carSpeed = 0
        self.carDir = [-1, 0]  # this is a unit vector
        self.carDirRad = 0  # radians

    def changeSpeed(self, always_active_bool):
        self.carSpeed += (1/(1 + self.carSpeed)) * 10 * always_active_bool
        """that bool determines the direction of the car, it can be -1 or 1"""

    def changeDir(self, always_active_bool):
        self.carDirRad += .3925 * always_active_bool
        """bool is -1 or 1, .785rad is 45 degrees"""
        self.carDir[0] = math.cos(self.carDirRad)
        self.carDir[1] = math.sin(self.carDirRad)

    def move(self, x, y):
        try:
            self.car.move(x, y)
            """checks to see if x and y are ints"""
        except (TypeError):
            print("Error: Invalid Operands in move (", x,",", y, ")")

    def act(self):
        super().act()
        self.move(self.carDir[0] * self.carSpeed, self.carDir[1] * self.carSpeed)

    def draw(self, window):
        self.car.draw(window)

class Wall(Object):
    def __init__(self, pt_a, pt_b):
        self.name = "Wall"
        self.a = Lines_and_Dist.Pt(pt_a.x, pt_a.y)
        self.b = Lines_and_Dist.Pt(pt_b.x, pt_b.y)
        self.line = Line(pt_a, pt_b)
        self.mathLine = Lines_and_Dist.MathLine(self.a, self.b)

    def draw(self, window):
        self.line.draw(window)

    def act(self):
        pass