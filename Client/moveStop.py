#!/usr/bin/env python3
from ev3dev.auto import *

left = LargeMotor(OUTPUT_A)
right = LargeMotor(OUTPUT_B)
spinner = MediumMotor(OUTPUT_C)

def move_stop(payload):
    left.duty_cycle_sp=0
    right.duty_cycle_sp=0

    left.run_direct()
    right.run_direct()

    if payload == 1:
        spinner.duty_cycle_sp=0
        spinner.run_direct()
