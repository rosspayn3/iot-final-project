#!/usr/bin/env python3

# *****************************************
# Name:         Ross Payne
# Problem Set:  Final Project
# Due Date:     Dec 16, 2021
# *****************************************

import os
import RPi.GPIO as GPIO
import cherrypy
from gpiozero import DistanceSensor, Buzzer
from time import sleep, time
from datetime import datetime

ds18b20 = ''

def setup():
        global ds18b20
        for i in os.listdir('/sys/bus/w1/devices'):
                if i != 'w1_bus_master1':
                        ds18b20 = '28-01201f7b8363'

distanceSensor = DistanceSensor(echo=22, trigger=23)  # board pins 15, 16
buzzer = Buzzer(24, active_high=False)  # board pin 18

def alert(duration):
    startTime = time()
    buzzer.beep(0.5, 0.25)

    while time() - startTime <= duration:
        sleep(0.1)

    buzzer.off()

def readDistance():
    distance = distanceSensor.distance * 100
    return distance

def readTemp():
        location = '/sys/bus/w1/devices/' + ds18b20 + '/w1_slave'
        tfile = open(location)
        text = tfile.read()
        tfile.close()
        secondline = text.split("\n")[1]
        temperaturedata = secondline.split(" ")[9]
        temperature = float(temperaturedata[2:])
        temperature = temperature / 1000
        return temperature

DHTPIN = 17 # board pin 11

GPIO.setmode(GPIO.BCM)

MAX_UNCHANGE_COUNT = 100

STATE_INIT_PULL_DOWN = 1
STATE_INIT_PULL_UP = 2
STATE_DATA_FIRST_PULL_DOWN = 3
STATE_DATA_PULL_UP = 4
STATE_DATA_PULL_DOWN = 5

def readHumidity():
        GPIO.setup(DHTPIN, GPIO.OUT)
        GPIO.output(DHTPIN, GPIO.HIGH)
        sleep(0.05)
        GPIO.output(DHTPIN, GPIO.LOW)
        sleep(0.02)
        GPIO.setup(DHTPIN, GPIO.IN, GPIO.PUD_UP)

        unchanged_count = 0
        last = -1
        data = []
        while True:
                current = GPIO.input(DHTPIN)
                data.append(current)
                if last != current:
                        unchanged_count = 0
                        last = current
                else:
                        unchanged_count += 1
                        if unchanged_count > MAX_UNCHANGE_COUNT:
                                break

        state = STATE_INIT_PULL_DOWN

        lengths = []
        current_length = 0

        for current in data:
                current_length += 1

                if state == STATE_INIT_PULL_DOWN:
                        if current == GPIO.LOW:
                                state = STATE_INIT_PULL_UP
                        else:
                                continue
                if state == STATE_INIT_PULL_UP:
                        if current == GPIO.HIGH:
                                state = STATE_DATA_FIRST_PULL_DOWN
                        else:
                                continue
                if state == STATE_DATA_FIRST_PULL_DOWN:
                        if current == GPIO.LOW:
                                state = STATE_DATA_PULL_UP
                        else:
                                continue
                if state == STATE_DATA_PULL_UP:
                        if current == GPIO.HIGH:
                                current_length = 0
                                state = STATE_DATA_PULL_DOWN
                        else:
                                continue
                if state == STATE_DATA_PULL_DOWN:
                        if current == GPIO.LOW:
                                lengths.append(current_length)
                                state = STATE_DATA_PULL_UP
                        else:
                                continue
        if len(lengths) != 40:
                #print ("Data not good, skip")
                return False


        shortest_pull_up = min(lengths)
        longest_pull_up = max(lengths)
        halfway = (longest_pull_up + shortest_pull_up) / 2
        bits = []
        the_bytes = []
        byte = 0

        for length in lengths:
                bit = 0
                if length > halfway:
                        bit = 1
                bits.append(bit)
        #print ("bits: %s, length: %d" % (bits, len(bits)))
        for i in range(0, len(bits)):
                byte = byte << 1
                if (bits[i]):
                        byte = byte | 1
                else:
                        byte = byte | 0
                if ((i + 1) % 8 == 0):
                        the_bytes.append(byte)
                        byte = 0
        #print (the_bytes)
        checksum = (the_bytes[0] + the_bytes[1] + the_bytes[2] + the_bytes[3]) & 0xFF
        if the_bytes[4] != checksum:
                #print ("Data not good, skip")
                return False

        return the_bytes[0], the_bytes[2]


def destroy():
        GPIO.cleanup()

setup()
