import math
from math import sin, cos, sqrt, pow, pi

class Pt:
    def __init__(self, a, b, rads = 0):
        self.x = a
        self.y = b
        self.radian = rads
        self.dist = 0 #this will be arbitrary in some cases
        """this just initializes the point"""

    def makePointAngle(self, angle, length):
        new_x = (cos(angle) * length) + self.x
        new_y= (sin(angle) * length) + self.y
        return Pt(new_x, new_y, angle)

class PointClound:
    def __init__(self, points = [], resolution = 60):
        self.points = points
        self.resolution = resolution

    def setPoints(self, points):
        self.points = points

    def setResolution(self, resolution):
        self.resolution = resolution

    def append(self, point):
        self.points.append(point)

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

    def makePerpLine(self, start_point, length):
        """
        y = ax (from known start point)
        d = sqrt(x^2 + y^2)
          = sqrt(x^2 + (ax)^2)
        d^2 = (a^2 + 1)x^2
        x = sqrt(d^2/(a^2 + 1))
        """
        new_slope = pow(self.slope * -1, -1)
        delta_x = sqrt(pow(length/2, 2) / (pow(new_slope,2) + 1))
        delta_y = new_slope * delta_x
        return MathLine(Pt(start_point.x - delta_x, start_point.y - delta_y), Pt(start_point.x + delta_x, start_point.y + delta_y))

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

    def getPointAlongLine(self, length):
        if self.pt_A.x < self.pt_B.x:
            pt = self.pt_A
        else:
            pt = self.pt_B

        new_x = sqrt(pow(length, 2) / (pow(self.slope, 2) + 1))
        new_y = new_x * self.slope
        new_x += pt.x
        new_y += pt.y
        return Pt(new_x, new_y)

    def getMidpoint(self):
        return Pt((self.pt_A.x + self.pt_B.x) / 2, (self.pt_A.y + self.pt_B.y) / 2)



class Lidar:
    """range finder"""
    def __init__(self, pt_A = Pt(0,0), range = 200):
        """A is a coordinate, max_range is an int of some sort"""
        self.pos = pt_A
        self.range = range
        self.pointcloud = PointClound()
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
        if self.checkPointLine(line, self.pos):
            dist = self.getDistPoint(intercept_point)
            return dist

        else:
            dist_a = self.getDistPoint(line.pt_A)
            dist_b = self.getDistPoint(line.pt_B)
            if dist_a < dist_b:
                return dist_a
            else:
                return dist_b


    def getDistPoint(self, pt):
        if pt.x == None or pt.y == None:
            return 99999
        else:
            x = self.pos.x
            y = self.pos.y
            dist = sqrt(pow(x - pt.x, 2) + pow(y - pt.y, 2))
            return dist

    def getIntersect(self, lidar_line, other_line):
        """a and b are lines"""
        if lidar_line.slope == other_line.slope:
            """a and b are parallel"""
            return None
        """m_0x + b_0 = m_1x + b_1"""
        """(m0 - m1)x = b1-b0"""
        """x = (b1-b0)/(m0-m1)"""

        try:
            x = (other_line.y_intercept - lidar_line.y_intercept) / (lidar_line.slope - other_line.slope)
            y = (lidar_line.slope * x) + lidar_line.y_intercept
            new_pt = Pt(x, y)
            if self.checkPointLine(lidar_line, new_pt) and self.checkPointLine(other_line, new_pt):
                return new_pt
            else:
                #no intersection
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
            if range[0] < pt.y or range[1] >= pt.y:
                return 1
            else:
                return 0
        else:
            return 0


    def scan(self, track, resolution = 60, starting_angle = 0):
        """track is an array of all of the math walls"""
        """This function generates a pointcloud around a user object"""
        self.pointcloud.setResolution(resolution)
        self.pointcloud.points = []
        angle = round(starting_angle * 180)
        if angle < 0:
            angle = (angle % -360) + 360
        else:
            angle = angle % 360
        angle_delta = (360/resolution)
        lidar_line = MathLine(self.pos, self.pos.makePointAngle(starting_angle, self.range))
        test_pt_array = []
        pt_flag = 0
        for x in range(0, resolution):
            test_pt_array = []
            for wall in track:
                test_pt = self.getIntersect(lidar_line, wall)
                if test_pt != None:
                    test_pt.radian = angle * math.pi/360
                    test_pt.dist = self.getDistPoint(test_pt)
                    test_pt_array.append(test_pt)
                    pt_flag = 1

            if pt_flag == 0:
                placeholder_pt = Pt(0, 0, 99999)
                # that is a point to use instead of "None"
                self.pointcloud.append(placeholder_pt)
            else:
                pt_flag = 0
                min = 99999
                min_index = 0
                for pt in test_pt_array:
                    if pt.dist < min:
                        min = pt.dist
                        min_index = test_pt_array.index(pt)
                self.pointcloud.append(test_pt_array[min_index])
            angle += angle_delta
            lidar_line.rotate(angle)
        return self.pointcloud


