import mediapipe as mp
import cv2,time
import pyautogui as gui
gui.FAILSAFE=False
video = cv2.VideoCapture(0)
mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils
ptime=0
ctime=0
change=False
value=30
movement=0,0
while True:
    currentPos=gui.position()
    succes, img = video.read()
    imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results=hands.process(imgRGB)
    if results.multi_hand_landmarks:
        handL = results.multi_hand_landmarks[0]
        landmarks=handL.landmark
        x,y=currentPos
        if abs(movement[0]-landmarks[8].x)*10>0.5:
            if (movement[0]-landmarks[8].x)*10>0.5:
                x+=value
            elif (movement[0]-landmarks[8].x)*10<0.5:
                x-=value
            change=True
        
        if abs(movement[1]-landmarks[8].y)*10>0.5:
            if (movement[1]-landmarks[8].y)*10>0.5:
                y-=value
            elif (movement[1]-landmarks[8].y)*10<0.5:
                y+=value
            change=True
        if change:
            gui.moveTo(x,y)
        if abs(landmarks[8].x-landmarks[4].x)<0.05 and abs(landmarks[8].y-landmarks[4].y)<0.05:
            gui.click()
        elif abs(landmarks[20].x-landmarks[4].x)<0.05 and abs(landmarks[20].y-landmarks[4].y)<0.05:
            value+=5
        elif abs(landmarks[12].x-landmarks[4].x)<0.05 and abs(landmarks[20].y-landmarks[4].y)<0.05:
            value-=5
        mpDraw.draw_landmarks(img,handL,mpHands.HAND_CONNECTIONS)
        movement=(landmarks[8].x,landmarks[8].y)
            
    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    cv2.putText(img,f'FPS : {int(fps)} Value = {value}',(10,70),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),3)
    cv2.imshow('Image',img)
    cv2.waitKey(1)