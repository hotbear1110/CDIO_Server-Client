#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import Client.ballCage
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

from ev3dev2.sound import Sound

spkr = Sound()

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    spkr.play_song((
    ('D4', 'e3'),
    ('D4', 'e3'),
    ('D4', 'e3'),
    ('G4', 'h'),
    ('D5', 'h')
))
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
    client.subscribe("spinForward")
    client.subscribe("spinBackward")
       
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
    elif msg.topic == "spinForward":
        Client.ballCage.spin_forward()
    elif msg.topic == "spinBackward":
        Client.ballCage.spin_backward()
client = mqtt.Client("Subscriber")
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message

client.loop_forever()
