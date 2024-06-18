#!/usr/bin/env python3
from ev3dev.auto import *

#Varibles
speed = 25

#Initiialize motor
right = LargeMotor(OUTPUT_B)

#move_left function
def move_right_backward():
    right.duty_cycle_sp=-speed
    right.run_direct()