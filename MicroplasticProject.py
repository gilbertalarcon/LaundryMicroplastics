# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 16:25:23 2021

@author: gilbe
"""
import tkinter as tk
import vc2 as vc
import cv2
import numpy as np



path=r"C:/Users/gilbe/OneDrive/BIOL 667/ProjectImages/poly_water3.jpg"
img=cv2.imread(path)

xRez=640; yRez=480;
displayScale=1 # scale display output
window=[0,yRez,0,xRez]
winInc=10 # pixels
frameCount=0
Z=64
CROP=25
BUTTON_WIDTH=10  # button display width
WINDOW_SCALE=10   # window size increment
Z_SCALE=0.0001 # convert integer Z units to 50 um
FULL_SCALE=2   # reduce full scale image by this factor so it fits in window
xc=1082; yc=468;     # center of crop window

vgaIM = cv2.resize(img, (xRez, yRez))

# blur and threshold image
thresh=90
blur=7
grayIM = cv2.cvtColor(vgaIM, cv2.COLOR_BGR2GRAY)     # convert color to grayscale image
blurIM=cv2.medianBlur(grayIM,blur)                 # blur image to fill in holes to make solid object
ret,threshIM = cv2.threshold(blurIM,thresh,255,cv2.THRESH_BINARY_INV) # threshold image to make pixels 0 or 255

thick=2     # bounding box line thickness
R=0         # red channel of bounding box line
G=255       # green channel of bounding box line
B=255       # blue channel of bounding box line
minArea=600
objCount=0



contourList, hierarchy = cv2.findContours(threshIM, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
for objContour in contourList:
                area=cv2.contourArea(objContour)
                if area > minArea:
                        objCount += 1
                        PO = cv2.boundingRect(objContour)
                        x0=PO[0]; y0=PO[1]; w=PO[2]; h=PO[3]
                        grayROI=grayIM[y0:y0+h,x0:x0+w]
                        cv2.rectangle(vgaIM, (x0,y0), (x0+w,y0+h), (B,G,R), thick) # place rectangle around each object
                        cv2.drawContours(vgaIM, objContour,-1, (0,0,255), thick)  # draw RED countour around object





cv2.imshow('vgaIM', vgaIM)
print(objCount)



cv2.waitKey(0)



