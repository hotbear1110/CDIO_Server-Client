#!/usr/bin/env python3
from ev3dev.auto import *

m = MediumMotor(OUTPUT_C)

def move_forward():
    m.duty_cycle_sp=50
    m.run_direct()