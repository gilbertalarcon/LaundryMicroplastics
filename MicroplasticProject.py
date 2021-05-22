# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 16:25:23 2021

@author: gilbe
"""
import tkinter as tk
import vc2 as vc
import cv2
import numpy as np



path=r"C:/Users/gilbe/OneDrive/BIOL 667/ProjectImages/NAL_210429_OwH2O_e.jpg"
img=cv2.imread(path)

xRez=640; yRez=480;
displayScale=1 # scale display output
window=[0,yRez,0,xRez]
winInc=10 # pixels
frameCount=0
Z=64
#CROP=25
BUTTON_WIDTH=10  # button display width
WINDOW_SCALE=10   # window size increment
Z_SCALE=0.0001 # convert integer Z units to 50 um
FULL_SCALE=2   # reduce full scale image by this factor so it fits in window
xc=1082; yc=468;     # center of crop window

vgaIM = cv2.resize(img, (xRez, yRez))

# blur and threshold image
thresh=90
blur=7
arearatio=5
grayIM = cv2.cvtColor(vgaIM, cv2.COLOR_BGR2GRAY)     # convert color to grayscale image
blurIM=cv2.medianBlur(grayIM,blur)                 # blur image to fill in holes to make solid object
ret,threshIM = cv2.threshold(blurIM,thresh,255,cv2.THRESH_BINARY_INV) # threshold image to make pixels 0 or 255


hsvImg= cv2.cvtColor(img,cv2.COLOR_BGR2HSV)


thick=2     # bounding box line thickness
R=0         # red channel of bounding box line
G=255       # green channel of bounding box line
B=255       # blue channel of bounding box line
minArea=300
objCount=0



contourList, hierarchy = cv2.findContours(threshIM, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
for objContour in contourList:
                area=cv2.contourArea(objContour)
                if area > minArea:
                        PO = cv2.boundingRect(objContour)
                        x0=PO[0]; y0=PO[1]; width=PO[2]; height=PO[3]
                        #print(area)
                        #print("width="+str(width))
                        #print("height="+str(height))
                        longest=max(width,height)
                        squareArea=longest*longest
                        #print(squareArea)
                        if squareArea/area > arearatio:
                            h=[]
                            s=[]
                            v=[]
                            objCount += 1
                            grayROI=grayIM[y0:y0+height,x0:x0+width]
                            cv2.rectangle(vgaIM, (x0,y0), (x0+width,y0+height), (B,G,R), thick) # place rectangle around each object
                            cv2.drawContours(vgaIM, objContour,-1, (0,0,255), thick)  # draw RED countour around object
                            hi = hsvImg[x0:x0+width,y0:y0+height, 0] #2W by 2W HSV img
                            h=np.append(h, int(np.average(hi)))
                            #print(hi)
                            si = hsvImg[x0:x0+width,y0:y0+height, 1] #2W by 2W HSV img   
                            s=np.append(s,int(np.average(si)))
                            #print(si)
                            vi = hsvImg[x0:x0+width,y0:y0+height, 2] #2W by 2W HSV img
                            v=np.append(v, int(np.average(vi)))
                            #print(vi)
                            print(h)
                            print()
                            print(s)
                            print()
                            print(v)
                            print()
                            if s > 180:
                                print("This is a polyester sample.")
                            else:
                                print("This is a cotton sample")
                                




cv2.imshow('vgaIM', vgaIM)
cv2.imshow('HSVIM', hsvImg)
print("Objects detected: " + str(objCount))



key = cv2.waitKey(0)
if key == ord("c"):
        cv2.destroyAllWindows()


