#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time

MQTT_Broker = '192.168.94.34'

client = mqtt.Client("publisher")
client.connect(MQTT_Broker,1883,60)

def sendMoveForward():
  client.publish("moveForward", 0)

def sendMoveBackward():
  client.publish("moveBackward", 0)

def sendMoveLeft():
  client.publish("moveLeft", 0)

def sendMoveLeftBackward():
  client.publish("moveLeftBackward", 0)

def sendMoveLeftMotor():
  client.publish("moveLeftMotor", 0)

def sendMoveRight():
  client.publish("moveRight", 0)

def sendMoveRightBackward():
  client.publish("moveRightBackward", 0)

def sendMoveRightMotor():
  client.publish("moveRightMotor", 0)

def sendMoveStop():
  client.publish("moveStop", 0)

def sendMoveWiggle():
  client.publish("moveWiggle", 0)

client.loop_forever()
