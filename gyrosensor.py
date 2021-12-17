#!/usr/bin/python3

# *****************************************
# Name:         Ross Payne & Jacob Baltazar
# Problem Set:  Final Project
# Due Date:     Dec 16, 2021
# *****************************************


import smbus2 as smbus
import math
import time

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

# gyro_xout = read_word_2c(0x43)
# gyro_yout = read_word_2c(0x45)
# gyro_zout = read_word_2c(0x47)
