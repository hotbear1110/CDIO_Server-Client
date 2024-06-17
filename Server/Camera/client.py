#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
import camera
# This is the Publisher

"""
client = mqtt.Client("publisher")
client.connect("192.168.5.34",1883,60)
client.publish("topic/motor-A/dt", 100)
time.sleep(1)
client.publish("topic/motor-A/dt", 0)
time.sleep(1)

client.publish("topic/motor-A/dt", 100)
time.sleep(1)
client.publish("topic/motor-A/dt", 0)
time.sleep(1)
client.disconnect()
"""

def algo():
    global grid
    while True:
        for y in range(len(camera.grid.boxes[0])):
            for x in range(len(camera.grid.boxes)):
                if camera.grid.boxes[x][y].getName() == "WBall":
                   print("W", end=" ")
                elif camera.grid.boxes[x][y].getName() == "OBall":
                    print("O", end=" ")
                elif camera.grid.boxes[x][y].getName() == "Egg":
                    print("E", end=" ")
                elif camera.grid.boxes[x][y].getName() == "robot":
                    print("R", end=" ")
                elif camera.grid.boxes[x][y].getName() == "robotFront":
                    print("F", end=" ")
                elif camera.grid.boxes[x][y].getName() == "robotBack":
                    print("B", end=" ")
                elif camera.grid.boxes[x][y].getName() == "Goal-Small-":
                    print("S", end=" ")
                elif camera.grid.boxes[x][y].getName() == "Goal-Large-":
                    print("G", end=" ")
                elif camera.grid.boxes[x][y].getName() == "Obstacle":
                    print("|", end=" ")
                elif camera.grid.boxes[x][y].getName() == "Wall":
                    print("|", end=" ")
                else:
                    print(" ", end=" ")
            print("")
        time.sleep(1)


#Config location is:
#/etc/mosquitto/conf.d

#Use this to read log.
#tail -f /var/log/mosquitto/mosquitto.log