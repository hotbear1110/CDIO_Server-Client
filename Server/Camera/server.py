#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# MQTT_Broker = '192.168.1.156'
MQTT_Broker = '192.168.5.34'


client = mqtt.Client("publisher")
client.connect(MQTT_Broker,1883,60)

def sendMoveForward(payload=0):
  client.publish("moveForward", round(payload))

def sendMoveBackward(payload=0):
  client.publish("moveBackward", round(payload))

def sendMoveLeft(payload=0):
  client.publish("moveLeft", round(payload))

def sendMoveLeftBackward(payload=0):
  client.publish("moveLeftBackward", round(payload))

def sendMoveLeftMotor(payload=0):
  client.publish("moveLeftMotor", round(payload))

def sendMoveRight(payload=0):
  client.publish("moveRight", round(payload))

def sendMoveRightBackward(payload=0):
  client.publish("moveRightBackward", round(payload))

def sendMoveRightMotor(payload=0):
  client.publish("moveRightMotor", round(payload))

def sendMoveStop(payload=0):
  client.publish("moveStop", round(payload))

def sendMoveWiggle(payload=0):
  client.publish("moveWiggle", round(payload))


def sendSpinForward(payload=0):
  client.publish("spinForward", round(payload))

def sendSpinBackward(payload=0):
  client.publish("spinBackward", round(payload))

#client.loop_forever()
