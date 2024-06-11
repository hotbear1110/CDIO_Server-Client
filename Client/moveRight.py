#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Direction, Stop

# Variables
speed = -500

# Initialize the EV3 brick
ev3 = EV3Brick()

# Initialize the motor
right_motor = Motor(Port.B)

# Define the move_right function
def move_right():
    right_motor.run(speed)

# Call the function to move the motor
move_right()
