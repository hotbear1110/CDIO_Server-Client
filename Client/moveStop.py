#!/usr/bin/env python3
from ev3dev2.auto import *

left = LargeMotor(OUTPUT_A)
right = LargeMotor(OUTPUT_B)
spinner = MediumMotor(OUTPUT_C)

def move_stop(payload):
    left.stop_action = "brake"
    right.stop_action = "brake"

    left.reset(stop_action = "brake")
    right.reset(stop_action = "brake")

    if payload == 1:
        spinner.stop_action = "brake"
        spinner.reset(stop_action = "brake")

    
