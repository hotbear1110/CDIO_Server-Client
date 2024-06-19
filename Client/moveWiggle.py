#!/usr/bin/env python3
from ev3dev.auto import *
import time

# Create motor objects
left_motor = LargeMotor(OUTPUT_A)
right_motor = LargeMotor(OUTPUT_B)

# Variables
speed = payload 

# move_wiggle function
def move_wiggle():
    for i in range(4):  # repeats 4 times
        left_motor.run_timed(speed_sp=speed, time_sp=800, stop_action="coast")
        right_motor.run_timed(speed_sp=-speed, time_sp=800, stop_action="coast")
        left_motor.wait_while('running')
        right_motor.wait_while('running')
        time.sleep(0.1)
        right_motor.run_timed(speed_sp=speed, time_sp=800, stop_action="coast")
        left_motor.run_timed(speed_sp=-speed, time_sp=800, stop_action="coast")
        right_motor.wait_while('running')
        left_motor.wait_while('running')
        time.sleep(0.1)
