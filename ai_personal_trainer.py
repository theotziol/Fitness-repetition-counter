#By theotziol
''' Idea and code help from the 'Murtaza's Workshop - Robotics and AI' ytb Channel
https://www.youtube.com/c/MurtazasWorkshopRoboticsandAI'''

import mediapipe as mp
import cv2
import numpy as np
import time
import posedetector
import exercises


file = 'D:\\downloads\\1621582174175.mp4'
cap = cv2.VideoCapture(file)
ptime = 0
font = cv2.FONT_HERSHEY_SIMPLEX
detector = posedetector.posedetector()
resize = (360, 720)
w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

print(w,h)

#fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#out = cv2.VideoWriter('pull_ups.mp4',fourcc,20.0,(resize))
if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret,frame = cap.read()

    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    ctime = time.time()
    #frame = cv2.resize(frame, resize)
    frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)
    frame = cv2.resize(frame,(360,720))
    ex1 = exercises.pull_up(frame, detector)
    lmlist = ex1.re_lmlist()
    frame = ex1.re_frame()
    #frame = detector.findpose(frame,False)
    #lmlist = detector.findpoints(frame)
    if len(lmlist) != 0:
        #detector.findangle(frame,12,14,16,True,'right arm')
        #detector.findangle(frame,11,13,15,True,'left arm')
        counts = ex1.pull_upps()
        frame = ex1.re_frame()
        
    
    fps = 1/(ctime-ptime)
    ptime = ctime
    fps = int(fps)
    fps = str(fps)
    #cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3)
    cv2.putText(frame, 'reps: '+ str(int(counts)), (resize[0]//2,resize[1]-80), font, 1, (0, 0, 255), 2)
    #out.write(frame)
    cv2.imshow('frame',frame)
    
    if cv2.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
#out.release()
cv2.destroyAllWindows()



