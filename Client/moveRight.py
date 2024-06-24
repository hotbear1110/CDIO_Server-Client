#!/usr/bin/env python3
from ev3dev2.auto import *
from ev3dev2.sensor.lego import GyroSensor
from ev3dev2.sensor import INPUT_1


# Variables
speedright = 40  # Adjusted motor speeds for turning right
speedleft = -40
slow_speedright = 25  # Slower speed for fine-tuning the turn
slow_speedleft = -25
slowdown_threshold = 25  # Angle threshold to start slowing down

# Initialize the motors and gyro sensor

left_motor = Motor(OUTPUT_A)
right_motor = Motor(OUTPUT_B)
gyro_sensor = GyroSensor(INPUT_1)
gyro_sensor.MODE_GYRO_RATE = 'GYRO-RATE'
gyro_sensor.MODE_GYRO_ANG = 'GYRO-ANG'

gyro_sensor.mode = 'GYRO-ANG'


gyro_sensor = GyroSensor(INPUT_1)
gyro_sensor.calibrate()

def print_gyro_values():
    while True:
        print(" Angle: {}".format(gyro_sensor.angle))
        time.sleep(0.5)

def move_right(payload):
    # Reset the gyro sensor to 0 degrees
    gyro_sensor.mode = 'GYRO-CAL'  # Switch to calibration mode to reset the sensor
    time.sleep(0.5)  # Give it a moment to reset
    gyro_sensor.mode = 'GYRO-ANG'  # Switch back to angle mode


    target_angle = payload

    # Start the motors
    left_motor.run_direct()
    right_motor.run_direct()

    # Turn until the target angle is reached
    while True:
        # Read the current angle from the gyro sensor
        current_angle = gyro_sensor.value()
        print(" Angle: {}, Rate: {}".format(gyro_sensor.angle, gyro_sensor.rate))

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