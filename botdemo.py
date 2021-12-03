import os
import pickle
import time
from pathlib import Path

import cv2

dir_path = os.path.dirname(os.path.realpath(__file__))
face_detect = cv2.CascadeClassifier(dir_path + '/lbpcascade_frontalface_improved.xml')
dir_path = dir_path + '/faces/'
Path(dir_path).mkdir(parents=True, exist_ok=True)
cap = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("face-trainer.yml")
last_recorded_time = time.time()

with open("picklejar/face-labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_detect.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    curr_time = time.time()
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        print(x, y, w, h)
        color = (255, 0, 0)
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
        id_, conf = recognizer.predict(roi_gray)
        if conf <= 70:
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(frame, f'{name}: {conf}', (x, y), font, 1, color, stroke, cv2.LINE_AA)

    cv2.imshow('frame', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
