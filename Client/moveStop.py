#!/usr/bin/env python3
from ev3dev2.auto import *

left = LargeMotor(OUTPUT_A)
right = LargeMotor(OUTPUT_B)

def move_stop():
    #stop both motors
    left.stop(stop_action='hold')
    right.stop(stop_action='hold')

    #ensure both motors are stopped
    while left.state != [] or right.state != []:
        left.stop(stop_action='hold')
        right.stop(stop_action='hold')