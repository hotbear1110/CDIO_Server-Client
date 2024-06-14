#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from ev3dev.auto import *

# This is the Subscriber

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("moveBackward.py")
    client.subscribe("moveForward.py")
    client.subscribe("moveLeft.py")
    client.subscribe("moveLeftBackward.py")
    client.subscribe("moveLeftMotor.py")
    client.subscribe("moveRight.py")
    client.subscribe("moveRightBackward.py")
    client.subscribe("moveRightMotor.py")
    client.subscribe("moveStop.py")
    client.subscribe("moveWiggle.py")
       
def on_message(client, userdata, msg):
    msg.payload = msg.payload.decode("utf-8")
    print(msg.payload)
    if msg.topicName = "moveBackward.py"
    move_backward()
    elif msg.topicName = "moveForward.py"
    move_forward()
    elif msg.topicName = "moveLeft.py"
    move_left()
    elif msg.topicName = "moveLeftBackward"
    move_right_backward()
    elif msg.topicName = "moveLeftMotor"
    move_left_motor()
    elif msg-topicName = "moveRight"
    move_right()
    elif msg.topicName = "moveRightBackward.py"
    move_right_backward()
    elif msg.topicName = "moveRightMotor.py"
    move_right_motor()
    elif msg.topicName = "moveStop.py"
    move_stop()
    elif msg.topicName = "moveWiggle.py"
    move_wiggle()

client = mqtt.Client("Subscriber")
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message

m.run_direct()
m.duty_cycle_sp=0

client.loop_forever()
