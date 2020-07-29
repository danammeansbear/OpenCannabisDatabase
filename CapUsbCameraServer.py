# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 18:10:04 2020

@author: adam
"""
import cv2
import imagezmq
import os
#image_hub = imagezmq.ImageHub(open_port='tcp://192.168.1.68:55555')
#image_hub.connect('tcp://192.168.1.68:55555')
image_hub = imagezmq.ImageHub(open_port='tcp://127.0.0.1:5555', REQ_REP=False)

while True:
    rpi_name, frame = image_hub.recv_image()
    cv2.imshow(rpi_name, frame)
    vidcap = frame
    success,image = vidcap.read()
    count = 0
    while success:
        path = 'C:/Users/adam/Desktop/images'
        cv2.imwrite(os.path.join(path,"frame%d.jpg" % count), image)     # save frame as JPEG file      
        success,image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1
    cv2.waitKey(1)
count += 1
