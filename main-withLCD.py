#!/usr/bin/env python

import RPi.GPIO as GPIO
import ds18b20
import i2c_lcd1602
import paho.mqtt.client as mqtt
import time

broker_address = "test.mosquitto.org"
Topic = "personal-wave3-ry"

Trigger = 7

# initialize GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(Trigger, GPIO.OUT)

print("creating new instance")
client = mqtt.Client("pub2") #create new instance

print("connecting to broker")
client.connect(broker_address) #connect to broker

screen = i2c_lcd1602.Screen(bus=1, addr=0x27, cols=16, rows=2)

def destory():
   GPIO.cleanup()

def loop():
    while True:
       screen.cursorTo(0, 0)
       screen.println(line)
       t = ds18b20.ds18b20Read()
       t = round(t, 2)
       m = '%f' %t
       m = m[:5]
       screen.cursorTo(1, 0)
       screen.println(' Temp: ' + m + ' C  ')
       screen.clear()
       client.publish(Topic,'  Temp: ' + m + ' C  ')
       time.sleep(3)      

if __name__ == '__main__':
#   print 'MY HOME'
   line = " RPi SENSOR "
   screen.enable_backlight()
   screen.clear()
   try:
      loop()
   except KeyboardInterrupt:
        GPIO.cleanup()
        print ('The end !!')

