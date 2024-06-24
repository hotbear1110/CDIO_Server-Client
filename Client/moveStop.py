#!/usr/bin/env python3
from ev3dev.auto import *

left = LargeMotor(OUTPUT_A)
right = LargeMotor(OUTPUT_B)

def move_stop():
    left.duty_cycle_sp=0
    right.duty_cycle_sp=0

    left.run_direct()
    right.run_direct()

    while left_motor != 0 or right_motor != 0:
        left.duty_cycle_sp = 0
        right.duty_cycle_sp = 0
        left.run_direct()
        right.run_direct()