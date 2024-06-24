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
import signal
import sys
import threading

from ev3dev2.sound import Sound

spkr = Sound()
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    Client.moveStop.move_stop(1)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


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
    client.subscribe("spinForward")
    client.subscribe("spinBackward")

    spkr.play_file('startup.wav')
       
def on_message(client, userdata, msg):
    msg.payload = float(msg.payload.decode("utf-8"))
    print(msg.topic + " " + str(msg.payload))
    if msg.topic == "moveBackward":
        t1 = threading.Thread(target=Client.moveBackward.move_backward, args=[msg.payload])

        t1.start()
    elif msg.topic == "moveForward":
        t1 = threading.Thread(target=Client.moveForward.move_forward, args=[msg.payload])

        t1.start()
    elif msg.topic == "moveLeft":
        Client.moveLeft.move_left(msg.payload)
    elif msg.topic == "moveLeftBackward":
        Client.moveLeftBackward.move_left_backward(msg.payload)
    elif msg.topic == "moveLeftMotor":
        Client.moveLeftMotor.move_left_motor(msg.payload)
    elif msg.topic == "moveRight":
        Client.moveRight.move_right(msg.payload)
    elif msg.topic == "moveRightBackward":
        Client.moveRightBackward.move_right_backward(msg.payload)
    elif msg.topic == "moveRightMotor":
        Client.moveRightMotor.move_right_motor(msg.payload)
    elif msg.topic == "moveStop":
        Client.moveStop.move_stop(msg.payload)
    elif msg.topic == "moveWiggle":
        Client.moveWiggle.move_wiggle(msg.payload)
    elif msg.topic == "spinForward":
        Client.ballCage.spin_forward(msg.payload)
    elif msg.topic == "spinBackward":
        Client.ballCage.spin_backward(msg.payload)
def on_disconnect(client, userdata, flags, rc):
    Client.moveStop.move_stop(1)

client = mqtt.Client("Subscriber")
client.connect("localhost",1883,60)

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

client.loop_forever()
