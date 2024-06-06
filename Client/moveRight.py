from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

#Varibles
speed = 500

#Initialize brick
ev3 = EV3Brick

#Initiialize motor
right_motor = Motor(Port.B)

#move_left function
def move_right():
    right_motor(speed)

move_right()