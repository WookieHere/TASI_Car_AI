import Graphics_Handler
import Handlers
import Messager_Facade
import Linear_AI_Interface
import User_Interface

print("Program Start")
Framerate = 100 #this is frames per second
Test_AI = Linear_AI_Interface.AI_Interface()
Test_User = User_Interface.UserInterface()
Handler = Handlers.HeadlessHandler()
Graphics = Graphics_Handler.GHandler()
Handler.setRunLength(50)
Sim = Messager_Facade.Messager(Test_AI, Handler)
Sim.setFrameRate(Framerate, True)
Sim.loadMap("Box")
Sim.run()
print("Program Exiting...")


"""
Notes:
Update lidar to get point radians relative to current car angle
Add Exponential Node Template
Confirm Headless mode functionality for faster learning rate
FIX BEST_CONSTANTS SYSTEM IN FUNCTION HANDLER*
"""



