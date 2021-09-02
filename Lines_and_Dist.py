import math

import math

class Pt:
    x = 0
    y = 0

    def __init__(self, a, b):
        self.x = a
        self.y = b
        """this just initializes the point"""

class MathLine:

    def __init__(self, A, B):
        self.pt_A = A
        self.pt_B = B
        """the points A and B are the -endpoints-"""

        self.rise = (self.pt_A.y - self.pt_B.y)
        self.run = (self.pt_A.x - self.pt_B.x)
        self.slope = (self.pt_A.y - self.pt_B.y)/(self.pt_A.x - self.pt_B.x)

        self.y_intercept = (-self.pt_A.x * self.slope) + self.pt_A.y

class Lidar:
    """range finder"""
    def __init__(self, pt_A):
        """A is a coordinate, max_range is an int of some sort"""
        self.pos = pt_A
        self.range = 2000
        """range is just to prevent bugs in open spaces"""

    def getDistLine(self, line):
        recip_slope = -1/line.slope
        pos_y_intercept = (-self.pos.x * recip_slope) + self.pos.y
        """equ of the line is: y = mx + b"""
        """-y_1 + recip_slope * x_1 + y_int_1 = ..."""
        """Goes into: recip_slope * x + y_int_pos = line.slope * x + y_int... solve for x"""
        intercept_x = (-pos_y_intercept + line.y_intercept)/(recip_slope - line.slope)
        intercept_y = (intercept_x * recip_slope) + pos_y_intercept
        intercept_point = Pt(intercept_x, intercept_y)
        dist = self.getDistPoint(intercept_point)
        return dist

    def getDistPoint(self, pt):
        x = self.pos.x
        y = self.pos.y
        dist = math.sqrt(pow(x - pt.x, 2) + pow(y - pt.y, 2))
        return dist

    def findLine(self, slope, track):
        """data structure of track is sorted array by x's of lines"""