#!/usr/bin/env python
import pygame
import pygame.camera
from pygame.locals import *
from twython import Twython
from datetime import datetime
from twitter-config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

api = Twython(CONSUMER_KEY,CONSUMER_SECRET,ACCESS_KEY,ACCESS_SECRET)

date = datetime.now()
timestamp = date.strftime("%a %b %d, %Y %#I:%M:%S %p")

pygame.init()
pygame.camera.init()
cam = pygame.camera.Camera("/dev/video0",(720,540))
cam.start()
image = cam.get_image()
pygame.image.save(image,'webcam.jpg')

photo = open('webcam.jpg','rb')
api.update_status_with_media(media=photo, status='Movement detected at ' + timestamp)
