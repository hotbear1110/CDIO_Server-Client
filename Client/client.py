#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
# This is the Publisher

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

#Config location is:
#/etc/mosquitto/conf.d

#Use this to read log.
#tail -f /var/log/mosquitto/mosquitto.log