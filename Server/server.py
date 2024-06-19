#!/usr/bin/env python3

import paho.mqtt.client as mqtt

MQTT_Broker = '192.168.125.34'

client = mqtt.Client("publisher")
client.connect(MQTT_Broker,1883,60)

def sendMoveForward(payload=0):
  client.publish("moveForward", payload)

def sendMoveBackward(payload=0):
  client.publish("moveBackward", payload)

def sendMoveLeft(payload=0):
  client.publish("moveLeft", payload)

def sendMoveLeftBackward(payload=0):
  client.publish("moveLeftBackward", payload)

def sendMoveLeftMotor(payload=0):
  client.publish("moveLeftMotor", payload)

def sendMoveRight(payload=0):
  client.publish("moveRight", payload)

def sendMoveRightBackward(payload=0):
  client.publish("moveRightBackward", payload)

def sendMoveRightMotor(payload=0):
  client.publish("moveRightMotor", payload)

def sendMoveStop(payload=0):
  client.publish("moveStop", payload)

def sendMoveWiggle(payload=0):
  client.publish("moveWiggle", payload)


def sendSpinForward(payload=0):
  client.publish("spinForward", payload)

def sendSpinBackward(payload=0):
  client.publish("spinBackward", payload)

#client.loop_forever()
