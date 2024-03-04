import cv2
import dlib
import pyautogui as screen

import openThings
import tutorial

screen.FAILSAFE = False

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

sensitivity_x = 12
sensitivity_y = 12

adjustment_x = 205 # increase if cursor is far right from the center
adjustment_y = 185 # increase if cursor is far up from the center

screen.PAUSE=0

def CameraMouse():

    global activate_mouse  # Declare as global

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")

    cap = cv2.VideoCapture(0)  # 0 is index for webcams

    while True:
        _, frame = cap.read()

        flipped_frame = cv2.flip(frame, 1)

        gray = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)

        for face in faces:

            landmarks = predictor(gray, face)

            x1 = face.left()
            y1 = face.top()
            x2 = face.right()
            y2 = face.bottom()

            xx = landmarks.part(30).x
            yy = landmarks.part(30).y

            follow_x = xx - 205
            follow_y = yy - 185

            current_pos = screen.position()

            previous_x = xx
            previous_y = yy

            current_x = xx
            current_y = yy

            check_x = previous_x - current_x
            check_y = previous_y - current_y

            screen.moveTo(follow_x * sensitivity_x - current_x, follow_y * sensitivity_y - current_y, duration=0.1)

            cv2.rectangle(flipped_frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.circle(flipped_frame, (xx, yy), 3, (255, 0, 0), -1)

        cv2.imshow('Frame', flipped_frame)

        key = cv2.waitKey(1)
        if not openThings.activate_mouse:
            cap.release()
            cv2.destroyAllWindows()
            break