import cv2 
import mediapipe as mp
import time
import PoseModule as pm 
import math
import numpy as np
from audioplayer import AudioPlayer
import os

##########file upload ##############
musicPath = 'res\musics'
musicList = os.listdir(musicPath)
player = AudioPlayer(f'{musicPath}\{musicList[0]}')

imgPath = 'res\imgs'
backList = os.listdir(imgPath)
backImg = cv2.imread(f'{imgPath}\{backList[0]}')
imgList = os.listdir('res\imgButton')
imgButton = []
for i in imgList:
    imgs = cv2.imread(f'res\imgButton\{i}')
    imgs = cv2.resize(imgs,(50,50))
    imgButton.append(imgs)
imgPause = imgButton[4]
imgPlay = imgButton[10]

###############################################


###########Variables###################
detector = pm.poseDetection()
toggle = True
pTime = 0
vol = 50
volBar = 150
volPer = 0
pTime = 0
released = True
played = False
paused = False
straight = False
controlMode = True
draw = False
musicNum = 0
i=0
count = 0
mode = 'controlMode'
#######################################



###########Set up web cam##################
cap = cv2.VideoCapture(0)
cap.set(3,840)
cap.set(4,680)
######################################



def stop(stopOrPause = True):
    #True is stop false is pause
    if stopOrPause == True:
        player.stop()
    elif stopOrPause == False:
        player.pause()
    
    imgPlay = imgButton[10]
    imgPause = imgButton[3]


while True: 

    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findPose(img,draw=True)
    lmList = detector.findPosition(img)
    x,y,_ = img.shape
    imgNext = imgButton[2]
    imgPrev = imgButton[7]
    
    
    if len(lmList) != 0:
        if controlMode == True:
            
            mode = 'Control Mode'
            x1,y1 = lmList[19][1],lmList[19][2]
            x2,y2 = lmList[20][1], lmList[20][2]
            cx,cy = (x1+x2)//2,(y1+y2)//2
            length = math.hypot(x2-x1,y2-y1)
            
            
            #print(centerCircle)
            ####### When both arms are above sholders --> volume control############
            if (lmList[11][2] > lmList[19][2]) & (lmList[12][2] > lmList[20][2]):
                volPer = np.interp(length,[50,250],[0,100])
                col = np.interp(length,[50,190],[50,255])
                color = (255,col*0.8,0)
                if volPer<=0: color = (0,0,255) 
                elif volPer>=100: color = (0,255,0)
                cv2.circle(img,(x1,y1),25,color,cv2.FILLED)
                cv2.circle(img,(x2,y2),25,color,cv2.FILLED)
                cv2.circle(img,(cx,cy),30,color,cv2.FILLED)
                cv2.line(img,(x1,y1),(x2,y2),color,5)
                vol = np.interp(length,[50,250],[0,100])
                player.volume = vol

            ######### Right Arm #################
            elif (lmList[11][2]-50 > lmList[19][2]) & (lmList[12][2]-50 < lmList[20][2]):
                angle = detector.findAngle(img,11,13,19,draw=draw)
                imgNext = imgButton[0]
                if angle < 110: straight = True
                if angle > 150 and straight == True: 
                    player.stop()
                    imgPlay = imgButton[10]
                    imgPause = imgButton[3]
                    imgNext = imgButton[1]
                    if musicNum == len(musicList)-1:
                        musicNum = -1
                    musicNum = musicNum+1
                    player = AudioPlayer(f'{musicPath}\{musicList[musicNum]}')
                    backImg = cv2.imread(f'{imgPath}\{backList[musicNum]}')
                    #print(musicList[musicNum])
                    player.play(loop=True)
                    imgPlay = imgButton[8]
                    imgPause = imgButton[4]
                    paused = False
                    straight = False
                    
                    
            ########################################

            ######## Left Arm #######################
            elif (lmList[11][2]-50 < lmList[19][2]) & (lmList[12][2]-50 > lmList[20][2]):
                angle = detector.findAngle(img,12,14,20,draw=draw)
                imgPrev = imgButton[5]
                if angle > 220: straight = True
                if angle < 200 and straight == True:
                    player.stop()
                    imgPlay = imgButton[10]
                    imgPause = imgButton[3]
                    imgPrev = imgButton[6]
                    if musicNum == 0:
                        musicNum = len(musicList)
                    musicNum = musicNum-1
                    player = AudioPlayer(f'{musicPath}\{musicList[musicNum]}')
                    backImg = cv2.imread(f'{imgPath}\{backList[musicNum]}')
                    player.play(loop=True)
                    imgPlay = imgButton[8]
                    imgPause = imgButton[4]
                    paused = False
                    straight = False
                    
                    
            ########################################

            ############ if both arms are below sholders --->  Pause or Play #####################
            if (lmList[11][2] < lmList[19][2]) & (lmList[12][2] < lmList[20][2]):
                if length > 150: released = True
                if length < 50: 
                    if played == False:
                        player.play(loop=True)
                        imgPlay = imgButton[8]
                        imgPause = imgButton[4]
                        played=True
                        released=False
                    else:
                        if released == True:
                            if paused == False : 
                                player.pause()
                                imgPlay = imgButton[10]
                                imgPause = imgButton[3]
                                paused = True
                            else: 
                                player.resume()
                                imgPlay = imgButton[8]
                                imgPause = imgButton[4]
                                paused = False
                            released = False
        else:
            mode = 'Dance Mode'
        ############if right arm is closer to left sholder##############
        if (lmList[12][2]+70 > lmList[19][2] and lmList[12][2]-70 < lmList[19][2] and lmList[12][2]+70 >lmList[19][2] and lmList[12][1]-70 < lmList[19][1]): 
            i = i + 1
            if i%10 == 0 and count <= 5:
                count = count + 1
            if count == 4:
                if controlMode == True:
                    player.resume()
                    imgPlay = imgButton[8]
                    imgPause = imgButton[4]
                    controlMode = False
                elif controlMode == False:
                    controlMode = True
                
                count = 0
        else:
            i = 0
            count = 0
        cv2.putText(img,f'{musicNum+1}/{len(musicList)}',(530,65),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,0,),3)
        #print(f'shoulder:{lmList[12][1]}, wrist:{lmList[19][1]}')
        
    #print(f'musicNum:{musicNum}, music{musicList[musicNum]},image:{backList[musicNum]}')


            
        

   

    

    
    
   
    
    cv2.rectangle(img,(50,250),(60,550),(192,192,192), cv2.FILLED)
    cv2.circle(img,(55,int(550-vol*3)),15,(200,200,0),cv2.FILLED,)
    cv2.putText(img,f'{int(vol)}%',(35,600),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),3)
    cv2.putText(img,f'Mode: {mode}',(260,150),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),3)
    if count > 1:cv2.putText(img,f'Changing mode {4-count}s',(260,200),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,255),3)
    backImg = cv2.resize(backImg,(150,200))
    button = 250
    img[20:220,30:180]=backImg
    img[30:80,button:button+50] = imgPrev
    img[30:80,button+60:button+110] = imgPause
    img[30:80,button+60*2:button+50+60*2] = imgPlay
    img[30:80,button+60*3:button+50+60*3] = imgNext
    cv2.imshow('Output', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break