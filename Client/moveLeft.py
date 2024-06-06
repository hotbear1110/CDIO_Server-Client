from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

#Varibles
speed = 500

#Initialize brick
ev3 = EV3Brick

#Initiialize motor
left_motor = Motor(Port.A)

#move_left function
def move_left():
    left_motor(speed)

move_left()