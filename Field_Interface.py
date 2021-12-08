from Lines_and_Dist import *
from Car_Handler import *
from re import compile

class Field_Interface:
    def __init__(self):
        self.car_size = 50
        self.checkpoint = Pt(0, 0)
        self.walls = []
        self.Reward_Track = Reward_Track()
        self.Lidar = Lidar(Pt(0,0), 2000)
        self.Stall_Checker = Stall_Tracker(self.Lidar.pos)
        self.iteration_counter = 0
        self.current_fitness = 0
        self.pointcloud = []

    def checkCollision(self):
        """get user objects, check against wall objects using lidar"""
        collision_flag = 0
        for point in self.pointcloud.points:
            if self.Lidar.getDistPoint(point) < self.car_size + 10:
                collision_flag = True
                return True
                break
                #collision!
        if not collision_flag:
            return False

    def ruleCheck(self):
        self.iteration_counter += 1
        self.Stall_Checker.setCarPos(self.Lidar.pos)
        reason = self.Stall_Checker.checkStall(self.current_fitness)
        if self.checkCollision():
            self.current_fitness -= 10000
            self.iteration_counter = 0
            return True
        elif reason == "Pos_Stall":
            self.current_fitness -= 10000 * self.iteration_counter
            self.iteration_counter = 0
            return True
        elif reason == "Fit_Stall":
            self.current_fitness -= 11000
            return True
        else:
            return False


    def modify(self, cmdList):
        """this function will later run collision detection etc as a driver"""
        cmdList.append("end")
        return 1

    def getPointCloud(self, pos, start_angle = 0,  resolution = 8):
        self.Lidar.setPos(Pt(pos.x, pos.y))
        self.pointcloud = self.Lidar.scan(self.walls, resolution, start_angle)
        return self.pointcloud

    def addWall(self, cmd):
        regex = compile(r'\d+(?:\.\d+)?') #this pulls numbers out of a string
        coords = regex.findall(cmd)
        self.walls.append(MathLine(Pt(float(coords[0]), float(coords[1])), Pt(float(coords[2]), float(coords[3]))))
        pass

    def setCheckPoint(self, pos):
        self.checkpoint = Pt(pos.x, pos.y)

    def resetCar(self, car):
        car.move(self.checkpoint.x - car.pos.x, self.checkpoint.y - car.pos.y)
        car.setPos(self.checkpoint)
        car.resetMovement()
        self.current_fitness = 0
        self.Stall_Checker.saved_fit = -1

    def fitnessUpdate(self):
        checkpt = self.Reward_Track.findNearestCheckpoint(self.Lidar)
        if self.Reward_Track.pointInCheckpoint(self.Lidar, checkpt):
            if checkpt.visit_flag != 1:
                checkpt.setVisited()
                self.current_fitness += 100

    def fitnessFunc(self):
        self.Reward_Track.clearCheckpoints()
        return self.current_fitness

    def clearFitness(self):
        self.current_fitness = 0

class Reward_Track:
    def __init__(self):
        self.track = [] #this will be an array of lines
        self.checkpoints = []
        self.checkpoint_radius = 100
        self.checkpoint_spread = 30
        self.checkpoint_size = 100

    def setCheckPoints(self):
        for line in self.track:
            l = 0
            line_len = line.getMagnitude()
            while l < line_len:
                pt = line.getPointAlongLine(l)
                self.checkpoints.append(Checkpoint(line.makePerpLine(pt, self.checkpoint_size)))
                l += self.checkpoint_spread
        #sort checkpoints by x
        for x in self.checkpoints:
            for i in range(0, len(self.checkpoints) - 1):
                if self.checkpoints[i].getKey() > self.checkpoints[i+1].getKey():
                    self.checkpoints[i], self.checkpoints[i+1] = self.checkpoints[i+1], self.checkpoints[i]

    def findNearestCheckpoint(self, Lidar):
        length = len(self.checkpoints)
        base_2 = 2
        i = round(length / base_2)
        prev_i = 0
        while prev_i != i + 1 and prev_i != i - 1 and i < length - 1:
            base_2 *= 2
            if Lidar.pos.x + Lidar.pos.y < self.checkpoints[i].key:
                prev_i = i
                i -= round(length/base_2)
            else:
                prev_i = i
                i += round(length/base_2)
        #closest is at either [i] or [prev_i]
        if Lidar.getDistLine(self.checkpoints[i].line) < Lidar.getDistLine(self.checkpoints[prev_i].line):
            return self.checkpoints[i]
        else:
            return self.checkpoints[prev_i]

    def setTrack(self, objects):
        self.track = []
        for obj in objects:
            if obj.name == "TrackLine":
                self.track.append(obj.mathLine)

    def setTrackLine(self, pt_a, pt_b):
        self.track.append(MathLine(pt_a, pt_b))

    def drawTrack(self, graphics):
        for obj in self.track:
            graphics.addObject(TrackLine(Point(obj.pt_A.x, obj.pt_A.y), Point(obj.pt_B.x, obj.pt_B.y)))

    def drawCheckpoints(self, graphics):
        for obj in self.checkpoints:
            graphics.addObject(TrackLine(Point(obj.line.pt_A.x, obj.line.pt_A.y), Point(obj.line.pt_B.x, obj.line.pt_B.y)))

    def distToTrack(self, lidar):
        min = 99999
        dist = 0
        for line in self.track:
            dist = lidar.getDistLine(line)
            if dist < min:
                min = dist
        return min

    def pointInCheckpoint(self, Lidar, checkpoint):
        if Lidar.getDistLine(checkpoint.line) < self.checkpoint_radius:
            return True
        else:
            return False

    def clearCheckpoints(self):
        for checkpoint in self.checkpoints:
            checkpoint.clearVisited()

class Checkpoint:
    def __init__(self, mathline):
        self.line = mathline
        self.midpt = mathline.getMidpoint()
        self.x = self.midpt.x
        self.y = self.midpt.y
        self.key = self.x + self.y
        self.visit_flag = 0

    def setVisited(self):
        self.visit_flag = 1

    def clearVisited(self):
        self.visit_flag = 0

    def getKey(self):
        return self.key

    def getDist(self, pos):
        return self.line.getDistPoint(pos)



class Stall_Tracker:
    def __init__(self, pt = Pt(0, 0)):
        self.car_pos = pt
        self.iteration_count = 0
        self.fit_count = 0
        self.min_stall_length = 50
        self.min_fit_length = 100
        self.saved_pos = pt
        self.saved_fit = 0
        self.leniency = 20

    def setCarPos(self, pt):
        self.car_pos = pt

    def setSavedPos(self, pt):
        self.saved_pos = pt

    def checkStall(self, fitness):
        if self.iteration_count > self.min_stall_length:
            self.iteration_count = 0
            """
            if self.getStallDist() < self.leniency:
                self.setSavedPos(self.car_pos)
                return "Pos_Stall"
            """
            if self.fit_count > self.min_fit_length:
                if self.saved_fit == fitness:
                    self.setSavedPos(self.car_pos)
                    return "Fit_Stall"
                else:
                    self.fit_count = 0
            else:
                self.setSavedPos(self.car_pos)
                self.saved_fit = fitness
                self.fit_count += 1
                return False
        else:
            self.iteration_count += 1
            self.fit_count += 1


    def getStallDist(self):
        dist = sqrt(pow(self.car_pos.x - self.saved_pos.x, 2) + pow(self.car_pos.y - self.saved_pos.y, 2))
        return dist
