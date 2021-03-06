from operator import truediv
import cv2
from time import sleep
import HandTrackingModule as htm
import os
import autopy
import numpy as np
import math
import mediapipe as mp

#import modules
#variables
frameR=20 #frame rduction
frameR_x=800
frameR_y=110
wCam,hCam=1300 ,400
pTime=0
smoothening = 5 #need to tune
plocX, plocY=0,0
clocX,clocY=0,0
##########
cap=cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector=htm.handDetector(maxHands=1)
wScr, hScr=autopy.screen.size() 
while True:
    #1. find hand landmarks
    success, img = cap.read()
    img= detector.findHands(img)
    lmList,bbox =detector.findPosition(img)
    
    #2. get the tip of the index and middle finger
    if len(lmList)!=0:
        x1,y1 =lmList[8][1:]
        x2, y2=lmList[12][1:]
        #print(x1,y1,x2,y2)

    #3. check which finger is up
        fingers=detector.fingersUp()
        cv2.rectangle(img, (frameR_x, frameR_y), (wCam-frameR_x,hCam-frameR_y),(255,0,0),2)

    #4. check if it is finger is in moving. index= moving, index and middle=clicking
    #convert the coordinates to get correct position
        if fingers[1]==1 and fingers[2]==0:
            #moving mode
            
            
            x3= np.interp(x1,(frameR,wCam-frameR_x),(0,wScr))
            y3= np.interp(y1,(frameR,hCam-frameR_y),(0,hScr))

    #5.smoothen the values
            clocX=plocX+(x3-plocX)/smoothening
            clocY=plocY+(y3-plocY)/smoothening
    #move the mouse
        #flip all existing values on x axis

            autopy.mouse.move(wScr-clocX,clocY)
            cv2.circle(img,(x1,y1),10,(0,255,0),cv2.FILLED)
            plocX,plocY=clocX,clocY

    #check if in clicking  mode both middle and index gfiner are up 
        if fingers[1]==1 and fingers[2]==1:
            length, img, lineinfo=detector.findDistance(8,12,img)
            #print(length)
            if length<40:
                cv2.circle(img, (lineinfo[4],lineinfo[5]),7,(0,200,0),cv2.FILLED)
                autopy.mouse.click()
                sleep(0.3)

        if fingers[1]==1 and fingers[2]==2 and fingers[3]==3:
            length, img, lineinfo=detector.findDistance(8,12,img)
            if length<40:
                print("true")



    #show image
    cv2.imshow("Image",img)
    cv2.waitKey(1)