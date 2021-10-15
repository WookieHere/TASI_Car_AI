
import Messager_Facade
import Linear_AI_Interface
import User_Interface

print("Program Start")
Test_AI = Linear_AI_Interface.AI_Interface()
Test_User = User_Interface.UserInterface()
Sim = Messager_Facade.Messager(Test_AI)
Sim.loadMap("Diamond")
Sim.run()
print("Program Exiting...")



