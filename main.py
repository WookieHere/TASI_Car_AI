import Graphics_Handler
import Frame_Control
import User_Interface
import Car_Handler

window = Graphics_Handler.GHandler()
UI = User_Interface.UserInterface(window)
window.addUserObject("Car_Handler.Car()")

timer = Frame_Control.TimerInterrupt(window, UI, .0125)



