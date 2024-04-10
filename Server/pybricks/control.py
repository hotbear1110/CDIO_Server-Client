#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.messaging import BluetoothMailboxServer, TextMailbox
from pybricks.tools import wait

ev3 = EV3Brick()
left_motor = Motor(Port.A)
right_motor = Motor(Port.C)
indsamler = Motor(Port.D)

server = BluetoothMailboxServer()
mbox = TextMailbox("command", server)

ev3.speaker.beep()
print("Waiting for connection...")
server.wait_for_connection()
print("Connected!")

while True:
    mbox.wait()
    command = mbox.read()
    
    if command == "start_indsamler":
        # Run indsamler and perform any additional actions here
        indsamler.run(speed=800)
        # Example: Move forward
        left_motor.run(-200)
        right_motor.run(-200)
        wait(20000)  # Adjust timing as needed
        left_motor.stop()
        right_motor.stop()
        indsamler.stop()
        break  # Exit after action; adjust logic as needed for continuous operation

server.disconnect()
