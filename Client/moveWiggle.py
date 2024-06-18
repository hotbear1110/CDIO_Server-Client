#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait

# Variables
speedright = -800
speedleft = 800

# Initialize brick
ev3 = EV3Brick()

# Initialize motor
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)

# move_wiggle function
def move_wiggle():
    for i in range(4):  # repeats 4 times
        left_motor.run_time(speed, 800, then=Stop.COAST, wait=True)
        right_motor.run_time(speed, 800, then=Stop.COAST, wait=True)
        wait(500)
        right_motor.run_time(speed, 800, then=Stop.COAST, wait=True)
        left_motor.run_time(speed, 800, then=Stop.COAST, wait=True)
        wait(500)

move_wiggle()
