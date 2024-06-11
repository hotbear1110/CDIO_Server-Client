#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop

degrees = 90

# Instantiate the EV3 Brick
ev3 = EV3Brick()

# Initialize the grab motor on Port D
grab_motor = Motor(Port.C)

# Reset the angle of the motor
grab_motor.reset_angle(0)

# Function to spin the claw forward
def spin_claw_forward():
    grab_motor.run_target(500, degrees, then=Stop.HOLD, wait=True)
    grab_motor.reset_angle(0)

spin_claw_forward()

# Function to spin the claw backward
def spin_claw_backward():
    grab_motor.run_angle(500, -degrees, then=Stop.HOLD, wait=True)
    grab_motor.reset_angle(0)

spin_claw_backward()
