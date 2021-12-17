# *****************************************
# Name:         Ross Payne
# Problem Set:  Final Project
# Due Date:     Dec 16, 2021
# *****************************************

import random

def getFakeDistance():
    distance = random.uniform(8,25)
    return distance

def getFakeTemp():
    temp = random.uniform(-10,40)
    return temp

def getFakeHumidity():
    humidity = random.uniform(30,80)
    return humidity

def getFakeGyroX():
    x = random.uniform(0, 25)
    return x

def getFakeGyroY():
    y = random.uniform(0, 25)
    return y
