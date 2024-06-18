#!/usr/bin/env python3
from ev3dev.auto import *

spinner = MediumMotor(OUTPUT_C)

def spin_forward():
    spinner.duty_cycle_sp=50
    spinner.run_direct()

    def backward_forward():
    spinner.duty_cycle_sp=-50
    spinner.run_direct()