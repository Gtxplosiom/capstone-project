import cv2
import dlib
import pyautogui

class CameraMouse():

    mouse_is_active = False
    
    def __init__(self):

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor('package/assets/models/cv_stuff/facial_landmark_detection/shape_predictor_68_face_landmarks.dat')

        self.sensitivity_x = 12
        self.sensitivity_y = 12

        self.adjustment_x = 205 # increase if cursor is far right from the center
        self.adjustment_y = 185 # increase if cursor is far up from the center

        pyautogui.PAUSE = 0
        pyautogui.FAILSAFE = False

    def run_mouse(self):

        self.mouse_is_active = True

        cap = cv2.VideoCapture(0)  # 0 is index for webcams

        while self.mouse_is_active:
            ret, frame = cap.read()

            if not ret:
                print("error retrieving frames")
                break

            flipped_frame = cv2.flip(frame, 1)

            gray = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)

            faces = self.detector(gray)

            for face in faces:

                landmarks = self.predictor(gray, face)

                x1 = face.left()
                y1 = face.top()
                x2 = face.right()
                y2 = face.bottom()

                xx = landmarks.part(30).x
                yy = landmarks.part(30).y

                follow_x = xx - 205
                follow_y = yy - 185

                current_pos = pyautogui.position()

                previous_x = xx
                previous_y = yy

                current_x = xx
                current_y = yy

                check_x = previous_x - current_x
                check_y = previous_y - current_y

                pyautogui.moveTo(follow_x * self.sensitivity_x - current_x, follow_y * self.sensitivity_y - current_y, duration=0.1)

                cv2.rectangle(flipped_frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.circle(flipped_frame, (xx, yy), 3, (255, 0, 0), -1)

            cv2.imshow('Preview', flipped_frame)

            key = cv2.waitKey(1)

            if not self.mouse_is_active:
                break
            
        cap.release()
        cv2.destroyAllWindows()