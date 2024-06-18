#!/usr/bin/env python3
from ev3dev.auto import *

left = LargeMotor(OUTPUT_A)
right = LargeMotor(OUTPUT_B)

def move_forward():
    left.duty_cycle_sp=-50
    right.duty_cycle_sp=-50

    left.run_direct()
    right.run_direct()
