#!/usr/bin/env python3

import Camera.server as server
import time

server.sendMoveForward(50)

time.sleep(5)

server.sendMoveRight(90)

time.sleep(5)

server.sendMoveLeft(90)

"""
server.sendSpinForward()
server.sendMoveForward()
time.sleep(2)

server.sendMoveStop()
time.sleep(1)

server.sendMoveBackward()
time.sleep(2)

server.sendMoveStop()
time.sleep(1)

server.sendMoveWiggle()
time.sleep(2)

server.sendSpinBackward()

server.sendMoveStop()
time.sleep(1)

server.sendMoveRight()
time.sleep(1)

server.sendMoveStop()
time.sleep(1)

server.sendMoveLeft()
time.sleep(1)

server.sendMoveStop()
time.sleep(1)

server.sendMoveRightBackward()
time.sleep(1)

server.sendMoveStop()
time.sleep(1)

server.sendMoveLeftBackward()
time.sleep(1)

server.sendMoveStop()
time.sleep(1)

server.sendMoveRightMotor()
time.sleep(1)

server.sendMoveStop()
time.sleep(1)

server.sendMoveLeftMotor
time.sleep(1)
"""