
import mediapipe as mp
import cv2
import numpy as np
import time
import posedetector


class exercise():
    def __init__(self, img, detector):
        self.img = img
        self.detector = detector
        self.frame = detector.findpose(img,False)
        self.lmlist = detector.findpoints(img)

    def re_lmlist(self):
        return self.lmlist

    def re_frame(self):
        return self.frame
 

class pull_up(exercise):
    distance_point = 0
    dir = 0
    count = 0
    left_h =180
    right_h = 180

    def __init__(self, img, detector):
        super().__init__(img, detector)

    def find_by_angle(self,left,right):
        if left >= 220:
            left -= 180
        if right >= 220:
            right -= 180
  
        if left < 80 and right < 80 and pull_up.dir == 0:
            if pull_up.left_h > left and pull_up.right_h > right and self.distance_count(15):
                pull_up.left_h = left
                pull_up.right_h = right
                pull_up.count += 0.5
                pull_up.dir = 1
        if left >= 120 and right >=120 and pull_up.dir == 1:
            if pull_up.left_h < left and pull_up.right_h < right :
                pull_up.count += 0.5
                pull_up.left_h = left
                pull_up.right_h = right
                pull_up.dir = 0

        return pull_up.count

    #Validate by point coordinates
    def distance_count(self, point):
        thresh = 100
        cords = self.detector.find_cords(point)
        if pull_up.distance_point != 0:
            if pull_up.distance_point > cords[1] +thresh or \
                pull_up.distance_point > cords[1] -thresh:
                pull_up.distance_point = cords[1]
                high = True
            elif pull_up.distance_point < cords[1] +thresh or \
                pull_up.distance_point < cords[1] -thresh:
                high = False
            print(pull_up.distance_point, cords[1] )

            
        else: 
            pull_up.distance_point = cords[1]
            high = True

        return high


    def pull_upps(self):
        
        left_wrist = 15
        right_wrist = 16

        right_shoulder = 12
        left_shoulder = 11

        right_elbow = 14
        left_elbow = 13

        right_hip = 24
        left_hip = 23

        left = self.detector.findangle(self.img,left_wrist,left_elbow,left_shoulder)
        right = self.detector.findangle(self.img,right_wrist,right_elbow,right_shoulder)
        count = self.find_by_angle(left,right)
        self.frame = self.img
        return count