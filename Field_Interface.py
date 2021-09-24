from Lines_and_Dist import *
from re import compile

class Field_Interface:
    def __init__(self):
        self.walls = []
        self.Lidar = Lidar()
        self.pointcloud = []
        pass

    def checkCollision(self):
        """get user objects, check against wall objects using lidar"""
        pass

    def modify(self, cmdList):
        """this function will later run collision detection etc as a driver"""
        cmdList.append("end")
        return 1

    def getPointCloud(self, pos):
        self.Lidar.setPos(pos)
        self.pointcloud = self.Lidar.scan(self.walls)
        return self.pointcloud

    def addWall(self, cmd):
        regex = compile(r'\d+(?:\.\d+)?')
        coords = regex.findall(cmd)
        self.walls.append(MathLine(Pt(float(coords[0]), float(coords[1])), Pt(float(coords[2]), float(coords[3]))))
        pass
