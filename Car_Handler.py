from math import cos, sin
from Object_Handler import *
from Lines_and_Dist import *

class Car(UserObject):
    def __init__(self, pt = Pt(30, 30)):
        super().__init__()
        self.name = "Car"
        self.car = Rectangle(Point(pt.x - 20, pt.y - 20), Point(pt.x + 20, pt.y + 20))
        self.car.setFill('yellow') #only used with graphics
        self.carTopSpeed = 5
        self.carMaxTurnRate = .1 #this is in radians
        self.carMaxTurnTime = 5 # takes 5 frames to make wheel axis turn 45 degrees
        self.carSpeed = 0
        self.carDir = [-1, 0]  # this is a unit vector
        self.carDirRad = 0
        self.turnRate = 0
        self.pos = pt

    def changeSpeed(self, always_active_bool):
        lookahead_speed = self.carSpeed + (1 * always_active_bool)
        if lookahead_speed > self.carTopSpeed or lookahead_speed < -1 * self.carTopSpeed:
            pass
        else:
            self.carSpeed += 1 * always_active_bool
        #recently changed to negative

    def resetMovement(self):
        self.carSpeed = 0
        self.turnRate = 0
        self.carDirRad = 0
        self.carDir = [-1, 0]

        """that bool determines the direction of the car, it can be -1 or 1"""

    def changeDir(self, always_active_bool):
        if abs(self.turnRate + ((self.carMaxTurnRate/self.carMaxTurnTime) * always_active_bool)) < self.carMaxTurnRate:
            self.turnRate += (self.carMaxTurnRate/self.carMaxTurnTime) * always_active_bool
        """bool is -1 or 1, .785rad is 45 degrees"""
        #self.carDir[0] = cos(self.turnRate)
        #self.carDir[1] = sin(self.turnRate)

    def move(self, x, y):
        try:
            self.car.move(x, y)
            self.pos.x += x
            self.pos.y += y
            self.carDirRad += self.turnRate * self.carSpeed
            if self.carDirRad < 0:
                self.carDirRad += 2 * math.pi
            self.carDirRad = self.carDirRad % (2 * math.pi)
            self.carDir[0] = cos(self.carDirRad)
            self.carDir[1] = sin(self.carDirRad)

            """checks to see if x and y are ints"""
        except (TypeError):
            print("Error: Invalid Operands in move (", x,",", y, ")")

    def act(self):
        super().act()
        self.move(self.carDir[0] * self.carSpeed, self.carDir[1] * self.carSpeed)
        if self.turnRate != 0:
            self.turnRate = 0
            """
        if self.carDirRad > math.pi:
            self.carDirRad -= math.pi
        elif self.carDirRad < -math.pi:
            self.carDirRad += math.pi
            """

    def draw(self, window):
        self.car.draw(window)

    def getPos(self):
        return self.pos

    def setPos(self, pt):
        self.pos.x = pt.x
        self.pos.y = pt.y


class Wall(Object):
    def __init__(self, pt_a, pt_b):
        self.name = "Wall"
        self.a = Pt(pt_a.x, pt_a.y)
        self.b = Pt(pt_b.x, pt_b.y)
        self.line = Line(Point(pt_a.x, pt_a.y), Point(pt_b.x, pt_b.y))
        self.mathLine = MathLine(self.a, self.b)

    def draw(self, window):
        self.line.draw(window)

    def act(self):
        pass

class TrackLine(Wall):
    def __init__(self, pt_a, pt_b):
        super().__init__(pt_a, pt_b)
        #super was not working for some reason
        self.name = "TrackLine"
        self.line.setFill("green")
