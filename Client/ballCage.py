#!/usr/bin/env python3
from ev3dev.auto import *
import math

spinner = MediumMotor(OUTPUT_C)

def spin_forward(payload):
    spinner.duty_cycle_sp=-50
    spinner.run_direct()

def spin_backward(payload):
    spinner.duty_cycle_sp=50
    spinner.run_direct()

