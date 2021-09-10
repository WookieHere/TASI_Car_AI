

class Field_Interface:
    def __init__(self):
        pass

    def checkCollision(self):
        """get user objects, check against wall objects using lidar"""
        pass

    def modify(self, cmdList):
        """this function will later run collision detection etc as a driver"""
        cmdList.append("end")
        return 1