#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import time
import redis
import datetime

#broker_address = "127.0.0.1"
broker_address = "test.mosquitto.org"
#RedisHost = "127.0.0.1"
Topic = "personal-wave3-ry"

r = redis.Redis(host="myredis.ajcxn0.0001.apne1.cache.amazonaws.com", port='6379')

def on_message(client, userdata, message):
    date = datetime.datetime.now()
    txt = str(date.strftime("%Y-%m-%d %H:%M:%S"))
    m = str(message.payload.decode("utf-8"))
    print(txt,m)
    r.sadd('RPI Temperature',txt+m)
#    r.set('RPI Temp',m)
#    print("message topic=",message.topic)
#    print("message qos=",message.qos)
#    print("message retain flag=",message.retain)

print("creating new instance")
client = mqtt.Client("sub1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker

client.loop_start() #start the loop

while True:
    client.subscribe(Topic)
    time.sleep(2) # wait

client.loop_stop() #stop the loop


