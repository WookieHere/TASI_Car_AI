
from math import sin, cos, sqrt, pow, pi

class Pt:
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
        try:
            self.slope = (self.pt_A.y - self.pt_B.y)/(self.pt_A.x - self.pt_B.x)
        except (ZeroDivisionError):
            self.slope = 1000000 #arbitrary very high number

        self.y_intercept = (-self.pt_A.x * self.slope) + self.pt_A.y

    def getDomain(self):
        if(self.pt_A.x < self.pt_B.x):
            return self.pt_A.x, self.pt_B.x
        else:
            return self.pt_B.x, self.pt_A.x

    def getRange(self):
        if (self.pt_A.y < self.pt_B.y):
            return self.pt_A.y, self.pt_B.y
        else:
            return self.pt_B.y, self.pt_A.y

    def getMagnitude(self):
        return sqrt(pow(self.pt_A.x - self.pt_B.x, 2) + pow(self.pt_A.y - self.pt_B.y, 2))

    def rotate(self, angle):
        """rotates point b around point a, angle is in degrees"""
        rads = (angle/360) * 2*pi
        self.pt_B.x = (self.getMagnitude() * cos(rads)) + self.pt_A.x
        self.pt_B.y = (self.getMagnitude() * sin(rads)) + self.pt_A.y
        """update rise/run/slop fields"""
        self.rise = (self.pt_A.y - self.pt_B.y)
        self.run = (self.pt_A.x - self.pt_B.x)
        try:
            self.slope = (self.pt_A.y - self.pt_B.y) / (self.pt_A.x - self.pt_B.x)
        except (ZeroDivisionError):
            self.slope = 1000000  # arbitrary very high number

        self.y_intercept = (-self.pt_A.x * self.slope) + self.pt_A.y

class Lidar:
    """range finder"""
    def __init__(self, pt_A = Pt(0,0), range = 200):
        """A is a coordinate, max_range is an int of some sort"""
        self.pos = pt_A
        self.range = range
        self.pointcloud = []
        """range is just to prevent bugs in open spaces"""

    def setPos(self, pt_A):
        self.pos = pt_A

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
        dist = sqrt(pow(x - pt.x, 2) + pow(y - pt.y, 2))
        return dist

    def getIntersect(self, lidar_line, b):
        """a and b are lines"""
        if lidar_line.slope == b.slope:
            """a and b are parallel"""
            return None
        """m_0x + b_0 = m_1x + b_1"""
        """(m0 - m1)x = b1-b0"""
        """x = (b1-b0)/(m0-m1)"""

        try:
            x = (b.y_intercept - lidar_line.y_intercept) / (lidar_line.slope - b.slope)
            y = (lidar_line.slope * x) + lidar_line.y_intercept
            new_pt = Pt(x, y)
            if self.checkPointLine(b, new_pt):
                return new_pt
            else:
                return None

        except (AttributeError):
            print("ERROR: Lidar::getIntersect was not given two lines")
            return None

        except (ZeroDivisionError):
            print("ERROR: Parallel lines escaped filter check")

    def checkPointLine(self, line, pt):
        """This checks if a point is on a line"""
        domain = line.getDomain()
        range = line.getRange()
        if domain[0] < pt.x and domain[1] > pt.x:
            if range[0] < pt.y or range[1] > pt.y:
                return 1
            else:
                return 0
        else:
            return 0


    def scan(self, track, resolution = 60, starting_angle = 0):
        """track is an array of all of the math walls"""
        """This function generates a pointcloud around a user object"""
        angle = starting_angle
        lidar_line = MathLine(self.pos, Pt(self.pos.x + self.range, self.pos.y))

        for x in range(0, resolution):
            lidar_line.rotate(angle)
            for wall in track:
                test_pt = self.getIntersect(lidar_line, wall)
                if test_pt != None:
                    self.pointcloud.append(test_pt)
            angle = angle + (360/resolution)
        cloud = self.pointcloud
        self.pointcloud = []
        return cloud
    """There is a problem somewhere with the rotating process!!!"""

