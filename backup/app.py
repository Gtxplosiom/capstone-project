import cv2
import dlib
import numpy as np
import pyautogui as screen

cap = cv2.VideoCapture(0) #0 is index for webcams

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("files/shape_predictor_68_face_landmarks.dat")

x, y = screen.size() #used to get the screen size of the device. Used by the pyautogui library

#screen.PAUSE = 0

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, x) #used to set the video frame resolution to the same as the device
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, y)

while True:
    _, frame = cap.read()

    flipped_frame = cv2.flip(frame, 1) #value of 1 to flipped the target frame horizontally, and 0 to vertically flip

    gray = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY) #to convert image to gray for faster/easier processing

    faces = detector(gray)
    for face in faces:
        #x1 = face.left() #x1, y1, x2 and y2 is in order to specify the coordinates from detector output which looks like this: [(left, top) (right, bottom)]
        #y1 = face.top()
        #x2 = face.right()
        #y2 = face.bottom()

        ##cv2.rectangle(flipped_frame, (x1, y1), (x2, y2), (0,255,0), 3) #drawing of rectangle using cv2 syntax: cv2.rectangle(target_frame, (x1, y1), (x2, y2), (color_code), thickness)

        landmarks = predictor(gray, face)

        ##for n in range(0, 68): ## show all 68 facial landmarks based on the .dat file used
        ##    x = landmarks.part(n).x
        ##    y = landmarks.part(n).y
        ##    cv2.circle(flipped_frame, (x, y), 1, (0, 255, 0), -1)

        xx = landmarks.part(30).x #30 is the value of landmark point location based on the shape predictor used, in this case, the point of the nose
        yy = landmarks.part(30).y

        nX = 960 - xx #these two is the nth value to be added to xx and yy variables in order for the cursor to remain at the center no matter the movement
        nY = 540 - yy

        screen.moveTo(xx+640, yy+300) #used to move mouse on a coordinate

        cv2.circle(flipped_frame, (xx, yy), 3, (255, 0, 0), -1) #syntax: cv2.circle(target_frame, (x, y), thickness, (color_code), -1)

    cv2.imshow('Frame', flipped_frame) #syntax: cv2.imshow("name_of_frame", target_frame)

    key = cv2.waitKey(1)
    if key == 27: #27 is the "machine_value" for the esc key. This condition is used to exit the code
        break