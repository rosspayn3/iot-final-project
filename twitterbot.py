#!/usr/bin/env python

# *****************************************
# Name:         Ross Payne & Jacob Baltazar
# Problem Set:  Final Project
# Due Date:     Dec 16, 2021
# *****************************************

import pygame
import pygame.camera
import sys
import time
from pygame.locals import *
from twython import Twython
from datetime import datetime
from twitterconfig import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

args = sys.argv[1:]
message = ' '.join(args)

date = datetime.now()
timestamp = date.strftime("%d-%b-%Y (%H:%M:%S)")

pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(640,480))
print("starting webcam")
cam.start()
# camera sometimes take a second to start up
time.sleep(1)
image = cam.get_image()
print("saving image")
pygame.image.save(image,'webcam.jpg')

photo = open('webcam.jpg','rb')
print("uploading photo")
response = api.upload_media(media=photo)
print("photo uploaded")
print("updating status")

api.update_status(status = f"{timestamp} : {message}", media_ids=[response['media_id']])
print("status updated")
