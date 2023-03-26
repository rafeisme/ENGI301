#Quick test code to make sure button is wired correctly.

import time

import Adafruit_BBIO.GPIO as GPIO

GPIO.setup("USR3", GPIO.OUT)
GPIO.setup("P2_1", GPIO.IN)

while True:
    if GPIO.input("P2_1") < 1: 
        GPIO.output("USR3", GPIO.HIGH)
    else:
        GPIO.output("USR3", GPIO.LOW)