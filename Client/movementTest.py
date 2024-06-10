#!/usr/bin/env pybricks-micropython
# imports
from moveBackward import *
from moveForward import *
from moveLeft import *
from moveRight import *
from moveStop import *
from moveWiggle import *

# calling functions
move_forward()
wait(2000)

move_stop()

move_backward()
wait(2000)

move_stop()

move_left()
wait(2000)

move_stop()

move_right()
wait(2000)

move_stop()

move_wiggle()
wait(2000)

move_stop


