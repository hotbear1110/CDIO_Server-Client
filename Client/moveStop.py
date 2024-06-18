#!/usr/bin/env python3
from ev3dev.auto import *

left = LargeMotor(OUTPUT_A)
right = LargeMotor(OUTPUT_B)

def move_stop():
    left_motor.stop()
    right_motor.stop()
    break