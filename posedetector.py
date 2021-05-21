#You can find info for this code in 
# https://www.youtube.com/watch?v=brwgBf6VB0I&ab_channel=Murtaza%27sWorkshop-RoboticsandAI

import mediapipe as mp
import cv2
import numpy as np
import time
import math

font = cv2.FONT_HERSHEY_SIMPLEX
font2 = cv2.FONT_HERSHEY_PLAIN
resize = (1080,720)

class posedetector():
    def __init__(self, mode = False, MODEL_COMPLEXITY = 1, smooth = True,
                detectionCon = 0.5,trackCon=0.5):
        self.mode = mode
        self.MODEL_COMPLEXITY = MODEL_COMPLEXITY
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(self.mode, self.MODEL_COMPLEXITY, self.smooth, self.detectionCon, self.trackCon)

    def findpose(self, img, draw = True, connections = False):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(img)
        if self.results.pose_landmarks:
            if draw:
                if connections:
                    self.mp_draw.draw_landmarks(img,self.results.pose_landmarks,self.mp_pose.POSE_CONNECTIONS)
                else:
                    self.mp_draw.draw_landmarks(img,self.results.pose_landmarks)
        return img

    def findpoints(self, img, draw = False):
        self.landmarks_list = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = img.shape
                #print(id, lm)
                cx, cy = int(lm.x *w), int(lm.y * h)
                self.landmarks_list.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),12,(255,0,0),cv2.FILLED)
        return self.landmarks_list

    def findangle(self, img, p1, p2, p3, draw = True, angletext = ''):
        ''' find angle of 3 points'''
        x1,y1 = self.landmarks_list[p1][1:]
        x2,y2 = self.landmarks_list[p2][1:]
        x3,y3 = self.landmarks_list[p3][1:]

        angle = math.degrees(math.atan2(y3-y2,x3-x2)-
                             math.atan2(y1-y2,x1-x2))
        #if angle <0:
            #angle+=360
        #print(angle)
        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(255,255,255),2)
            cv2.line(img,(x2,y2),(x3,y3),(255,255,255),2)

            cv2.circle(img,(x1,y1),5,(0,0,255),cv2.FILLED)
            cv2.circle(img,(x1,y1),12,(0,0,255),2)

            cv2.circle(img,(x2,y2),5,(0,0,255),cv2.FILLED)
            cv2.circle(img,(x2,y2),12,(0,0,255),2)

            cv2.circle(img,(x3,y3),5,(0,0,255),cv2.FILLED)
            cv2.circle(img,(x3,y3),12,(0,0,255),2)

            text = '{} angle: {} degrees'.format(angletext, abs(int(angle)))
            cv2.putText(img,text,(x2-100,y2 +40),font2,1,(255,255,255),2)
        return abs(int(angle))

    def find_cords(self, point):
        '''compare two lines p1-p2/ p3-p4 for movement direction'''
        xi, yi = self.landmarks_list[point][1:]
        return xi,yi
        

def main():
    file = 'D:\\jiola\\downloads\\video.mp4'
    cap = cv2.VideoCapture(file)
    ptime = 0
    detector = posedetector()
    if not cap.isOpened():
        print("Cannot open camera")
        exit()
    while True:
        ret,frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        ctime = time.time()
        frame = cv2.resize(frame, resize)
        frame = detector.findpose(frame)
        lmlist = detector.findpoints(frame)
        print(len(lmlist))
        cv2.circle(frame,(lmlist[5][1],lmlist[5][2]),12,(255,0,0),cv2.FILLED)


        fps = 1/(ctime-ptime)
        ptime = ctime
        fps = int(fps)
        fps = str(fps)
        cv2.putText(frame, fps, (7, 70), font, 3, (100, 255, 0), 3)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) == ord('q'):
            break
# When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
