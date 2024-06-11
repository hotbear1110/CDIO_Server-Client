#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop
from pybricks.ev3dev2.motor import SpeedRPM

degrees = 90

# Instantiate the EV3 Brick
ev3 = EV3Brick()

# Initialize the grab motor on Port D
grab_motor = Motor(Port.D)

# Reset the angle of the motor
grab_motor.reset_angle(0)

# Function to spin the claw forward
def spin_claw_forward():
    grab_motor.run_target(100, degrees, then=Stop.HOLD, wait=True)
    grab_motor.reset_angle(0)

spin_claw_forward()

# Function to spin the claw backward
def spin_claw_backward():
    grab_motor.run_angle(100, -degrees, then=Stop.HOLD, wait=True)
    grab_motor.reset_angle(0)

spin_claw_backward()

def spin_claw_forever():
    grab_motor.run(800)

spin_claw_forever()

def spin_claw_stop():
    grab_motor.Stop

spin_claw_stop()

def spin_for_given_time():
    grab_motor.on_for_seconds(SpeedRPM(200),10)

spin_for_given_time()