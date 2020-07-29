# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 18:20:42 2020

@author: adam
"""

import cv2
import time
import socket 
from imutils.video import VideoStream
import imagezmq

#sender = imagezmq.ImageSender(connect_to='tcp://192.168.1.68:55555', REQ_REP=False)
# when using PUB/SUB, on sending computer, I specify *:5555 as address
sender = imagezmq.ImageSender('tcp://*:5555', REQ_REP=False)


# Open the device at the ID 0

cap = cv2.VideoCapture(0)
currentFrame = 0
#Check whether user selected camera is opened successfully.
if not (cap.isOpened()):
    print('Could not open video device')


rpi_name = socket.gethostname() # send RPi hostname with each image
#picam = VideoStream(usePiCamera=True).start()
#frame = VideoStream(usePiCamera=False).start()
time.sleep(2.0) # allow camera sensor to warm up
time.sleep(2.0)  # allow camera sensor to warm up
while True:  # send images as stream until Ctrl-C
        return_code, frame = cap.read()  # cap.read returns *2* args!!
        sender.send_image(rpi_name, frame)
        # print(rpi_name)
        # break     <<----- I had to comment out this line
