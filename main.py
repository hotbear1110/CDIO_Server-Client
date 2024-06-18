#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from ev3dev.auto import *
import Client.moveForward
import Client.moveBackward
import Client.moveLeft
import Client.moveLeftBackward
import Client.moveLeftMotor
import Client.moveRight
import Client.moveRightBackward
import Client.moveRightMotor
import Client.moveStop
import Client.moveWiggle

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("moveBackward")
    client.subscribe("moveForward")
    client.subscribe("moveLeft")
    client.subscribe("moveLeftBackward")
    client.subscribe("moveLeftMotor")
    client.subscribe("moveRight")
    client.subscribe("moveRightBackward")
    client.subscribe("moveRightMotor")
    client.subscribe("moveStop")
    client.subscribe("moveWiggle")
       
def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    print(msg.topic)
    if msg.topic == "moveBackward":
        Client.moveBackward.move_backward()
    elif msg.topic == "moveForward":
        Client.moveForward.move_forward()
    elif msg.topic == "moveLeft":
        Client.moveLeft.move_left()
    elif msg.topic == "moveLeftBackward":
        Client.moveLeftBackward.move_left_backward()
    elif msg.topic == "moveLeftMotor":
        Client.moveLeftMotor.move_left_motor()
    elif msg.topic == "moveRight":
        Client.moveRight.move_right()
    elif msg.topic == "moveRightBackward":
        Client.moveRightBackward.move_right_backward()
    elif msg.topic == "moveRightMotor":
        Client.moveRightMotor.move_right_motor()
    elif msg.topic == "moveStop":
        Client.moveStop.move_stop()
    elif msg.topic == "moveWiggle":
        Client.moveWiggle.move_wiggle()
client = mqtt.Client("Subscriber")
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
