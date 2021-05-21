# Fitness-repetition-counter
Fitness repetition counter
A CV counter for count repetition during workout. 
Dependecies OpenCV, MediaPose

*Currently it counts only Pull-Ups, more exercises will be added soon. Feel free to experiment and add exercises

For counting Pull-Ups I use the angle of 3 points (wrist, elbow, shoulder) using the pretrained model of mediapose to track landmarks of human body (posedetector) and I validate the rep by checking the coordinates of the landmarks.


