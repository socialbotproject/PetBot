import os
import time
from pathlib import Path

import cv2

dir_path = os.path.dirname(os.path.realpath(__file__))
face_detect = cv2.CascadeClassifier(dir_path + './recognizers/lbpcascade_frontalface_improved.xml')
cap = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
last_recorded_time = time.time()
name = input("Enter name to label face captures that are going to be saved ")
dir_path = dir_path + f'/faces/{name}/'
Path(dir_path).mkdir(parents=True, exist_ok=True)
imagenumber = 1
capped = 0

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detect.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    framealt = frame
    curr_time = time.time()
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 255)
    stroke = 2
    cv2.putText(frame, f'{imagenumber} saved faces, captured {capped} new ones', (0, 10), font, 0.6, color, stroke,
                cv2.LINE_AA)
    cv2.imshow('frame', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

    if curr_time - last_recorded_time >= 0.33:
        for (x, y, w, h) in faces:
            roi = frame[y:y + h, x:x + w]
            print(dir_path)

            while os.path.exists(dir_path + f"face{imagenumber}.jpg"):
                imagenumber += 1
            capped += 1
            cv2.imwrite(dir_path + f"face{imagenumber}.jpg", roi)
        last_recorded_time = curr_time

cap.release()
cv2.destroyAllWindows()
