#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor
from pybricks.parameters import Port
from pybricks.tools import wait

# Variables
speedright = -75  # Adjusted motor speeds for turning left
speedleft = 75
slow_speedright = -30  # Slower speed for fine-tuning the turn
slow_speedleft = 30
target_angle = -100  # Target angle to turn left
slowdown_threshold = 20  # Angle threshold to start slowing down

# Initialize the EV3 brick
ev3 = EV3Brick()

# Initialize the motors and gyro sensor
left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
gyro_sensor = GyroSensor(Port.S1)

# Reset the gyro sensor angle to 0
gyro_sensor.reset_angle(0)

# Define the move_left function
def move_left():
    # Start the motors
    right_motor.run(speedright)
    left_motor.run(speedleft)

    # Loop until the gyro sensor measures the target angle
    while gyro_sensor.angle() > target_angle:
        # Check if the angle is within the slowdown threshold
        if gyro_sensor.angle() > target_angle + slowdown_threshold:
            # Continue at full speed in reverse
            right_motor.run(speedright)
            left_motor.run(speedleft)
        else:
            # Slow down as the robot approaches the target angle in reverse
            right_motor.run(slow_speedright)
            left_motor.run(slow_speedleft)

        # Print the current gyro angle to the EV3 screen
        ev3.screen.clear()
        ev3.screen.draw_text(0, 0, "Angle: {}".format(gyro_sensor.angle()))

        # Print the current gyro angle to the terminal
        print("Angle: {}".format(gyro_sensor.angle()))
        
        wait(10)  # Small wait to avoid busy waiting

    # Stop the motors
    left_motor.stop()
    right_motor.stop()

# Call the function to move the motor
move_left()
