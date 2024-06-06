from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

#Speed variable
speed = 0

#Initialise brick
ev3 = EV3Brick

#Initialize motors
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

def move_stop():
    left_motor.run(speed)
    right_motor.run(speed)

move_stop()