#!/usr/bin/env python3
from ev3dev.auto import *

#Varibles
speed = payload

#Initiialize motor
right = LargeMotor(OUTPUT_B)

#move_left function
def move_right_motor():
    right.duty_cycle_sp=-speed
    right.run_direct()