#!/usr/bin/env python3

import paho.mqtt.client as mqtt

# This is the Publisher

client = mqtt.Client("publisher")
client.connect("192.168.1.94",1883,60)
client.publish("topic/motor-A/dt", 5)
client.disconnect()