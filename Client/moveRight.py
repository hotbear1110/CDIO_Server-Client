#!/usr/bin/env python3
from ev3dev.auto import *

# Variables
speedright = 25  # Adjusted motor speeds for turning right
speedleft = -25
slow_speedright = 16  # Slower speed for fine-tuning the turn
slow_speedleft = -16
target_angle = payload
slowdown_threshold = 45  # Angle threshold to start slowing down

# Initialize the motors and gyro sensor
left_motor = Motor(OUTPUT_A)
right_motor = Motor(OUTPUT_B)
gyro_sensor = GyroSensor(INPUT_1)
gyro_sensor.mode = 'GYRO-ANG'

def move_right():
    # Reset the gyro sensor to 0 degrees
    gyro_sensor.mode = 'GYRO-RATE'  # Temporarily switch to rate mode to reset the sensor
    gyro_sensor.mode = 'GYRO-ANG'  # Switch back to angle mode

    # Start the motors
    left_motor.run_direct()
    right_motor.run_direct()

    # Turn until the target angle is reached
    while True:
        # Read the current angle from the gyro sensor
        current_angle = gyro_sensor.value()

        # Check if we are close to the target angle
        if abs(target_angle - current_angle) <= slowdown_threshold:
            # If close to the target angle, use slow speed
            left_motor.duty_cycle_sp = slow_speedleft
            right_motor.duty_cycle_sp = slow_speedright
        else:
            # If not close to the target angle, use regular speed
            left_motor.duty_cycle_sp = speedleft
            right_motor.duty_cycle_sp = speedright

        # Check if we have reached the target angle
        if current_angle == target_angle:
            # Stop the motors
            left_motor.stop()
            right_motor.stop()
            break