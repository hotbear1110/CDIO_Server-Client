#!/usr/bin/env python3
from ev3dev.auto import *

left = LargeMotor(OUTPUT_A)
right = LargeMotor(OUTPUT_B)

def move_stop():
    left.duty_cycle_sp=payload
    right.duty_cycle_sp=payload

    left.run_direct()
    right.run_direct()
