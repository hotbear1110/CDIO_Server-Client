#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port

#Speed variable
speed = -500

# Initialize brick
ev3 = EV3Brick()

# Initialize motors
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

def move_forward():
    left_motor.run(speed)
    right_motor.run(speed)

move_forward()