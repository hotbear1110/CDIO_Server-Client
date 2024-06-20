#!/usr/bin/env python3

from moveForward import *
from moveBackward import *
from ballCage import *
from moveRight import *
from moveLeft import *
from moveStop import *
import time


spin_forward()
move_forward(50)

time.sleep(3)
move_stop()

time.sleep(2)
move_forward(50)

time.sleep(3)
move_stop()

time.sleep(2)
move_forward(50)

time.sleep(3)
move_stop()

time.sleep(2)
move_forward(50)

time.sleep(3)
move_stop()

time.sleep(2)
move_backward(50)

time.sleep(3)
move_stop()

time.sleep(2)
move_backward(50)

time.sleep(3)
move_stop()

time.sleep(2)
move_backward(50)

time.sleep(3)
move_stop()

time.sleep(2)
move_backward(50)

time.sleep(3)
move_stop()