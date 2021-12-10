#!/usr/bin/env python
import pygame
import pygame.camera
import time
import sys
from pygame.locals import *
from twython import Twython
from datetime import datetime
from twitterconfig import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET


api = Twython(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET)

args = sys.argv[1:]
message = ' '.join(args)
# print(f"🦆 message to tweet: '{message}'")

date = datetime.now()
timestamp = date.strftime("%a %b %d, %Y %#I:%M:%S %p")

pygame.init()
pygame.camera.init()

# Raspberry Pi OS
# cam = pygame.camera.Camera(0, (800,600))

# Windows
cam = 0
camlist = pygame.camera.list_cameras()
if camlist:
    cam = pygame.camera.Camera(camlist[0], (800,600))

cam.start()
# sleep a bit. sometimes it takes longer to capture an image.
time.sleep(0.5)
image = cam.get_image()
pygame.image.save(image, 'webcam.jpg')

photo = open('webcam.jpg','rb')
response = api.upload_media(media=photo)
api.update_status(status = f"{timestamp} : {message}", media_ids=[response['media_id']])
