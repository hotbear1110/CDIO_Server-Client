#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Direction, Stop

# Variables
speedright = 500
speedleft = -500

# Initialize the EV3 brick
ev3 = EV3Brick()

# Initialize the motor
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

# Define the move_right function
def move_left():
    right_motor.run(speedright)
    left_motor.run(speedleft)

# Call the function to move the motor
move_left()
