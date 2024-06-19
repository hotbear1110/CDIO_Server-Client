#!/usr/bin/env python3
from ev3dev.auto import *

#Varibles
speed = payload

#Initiialize motor
left = LargeMotor(OUTPUT_A)

#move_left function
def move_left_backward():
    left.duty_cycle_sp=-speed
    left.run_direct()