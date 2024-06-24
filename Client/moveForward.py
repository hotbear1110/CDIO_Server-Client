#!/usr/bin/env python3
from ev3dev.auto import *
import time

left = LargeMotor(OUTPUT_A)
right = LargeMotor(OUTPUT_B)
gyro_sensor = GyroSensor(INPUT_1)
gyro_sensor.mode = 'GYRO-ANG'

def move_forward(payload):

    # Reset the gyro sensor to 0 degrees
    gyro_sensor.mode = 'GYRO-CAL'  # Switch to calibration mode to reset the sensor
    time.sleep(0.5)  # Give it a moment to reset
    gyro_sensor.mode = 'GYRO-ANG'  # Switch back to angle mode

    left.duty_cycle_sp=-payload
    right.duty_cycle_sp=-payload

    left.run_direct()
    right.run_direct()

    while left.duty_cycle_sp != 0 and right.duty_cycle_sp != 0:

        current_angle = gyro_sensor.value()

        if current_angle < 0:
            left.duty_cycle_sp=-payload
            right.duty_cycle_sp = -payload + 10
        elif current_angle > 0:
            right.duty_cycle_sp=-payload
            left.duty_cycle_sp = -payload + 10
        else:
            left.duty_cycle_sp=-payload
            right.duty_cycle_sp=-payload
        
