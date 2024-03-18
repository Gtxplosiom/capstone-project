import cv2
import dlib
import numpy as np
from pynput.mouse import Button, Controller

mouse = Controller()

cap = cv2.VideoCapture(0) #0 is index for webcams

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("files/shape_predictor_68_face_landmarks.dat")

while True:
    _, frame = cap.read()

    flipped_frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:

        landmarks = predictor(gray, face)

        xx = landmarks.part(30).x
        yy = landmarks.part(30).y

        adjustedxx = xx+640
        adjustedyy = yy+300

        cv2.circle(flipped_frame, (xx, yy), 3, (255, 0, 0), -1)

    cv2.imshow('Frame', flipped_frame)

    key = cv2.waitKey(1)
    if key == 27:
        break