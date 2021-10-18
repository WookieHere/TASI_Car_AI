
import Messager_Facade
import Linear_AI_Interface
import User_Interface

print("Program Start")
Test_AI = Linear_AI_Interface.AI_Interface()
Test_User = User_Interface.UserInterface()
Sim = Messager_Facade.Messager(Test_AI)
Sim.setFrameRate(60, False)

Sim.loadMap("Maze")
Sim.run()
print("Program Exiting...")


"""
Notes:
Update lidar to get point radians relative to current car angle
Add Exponential Node Template
Add Handler for Motors etc. (This includes an abstract class "handler")
Confirm Headless mode functionality for faster learning rate
Adjust penalties for running into a wall vs stalling (reduce stalling rate)
"""



