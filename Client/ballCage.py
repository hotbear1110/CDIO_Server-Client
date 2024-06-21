#!/usr/bin/env python3
from ev3dev.auto import *
import math

spinner = MediumMotor(OUTPUT_C)

def spin_forward(payload):
    spinner.duty_cycle_sp=-50
    spinner.run_direct()

def spin_backward(payload):
    print(spinner.position)
    newPos = math.floor(spinner.position/spinner.count_per_rot)*spinner.count_per_rot
    print(newPos)
    spinner.run_to_abs_pos(position_sp=newPos, speed_sp=400, stop_action="brake")

