import os
import pickle

import cv2
import numpy as np
from PIL import Image

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "your beautiful face")

recognizer = cv2.face.LBPHFaceRecognizer_create()
current_id = 0

label_ids = {}
y_labels = []
x_train = []
for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(" ", "-").lower()
            print(label, path)
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]
            pil_image = Image.open(path).convert('L')
            imagearr = np.array(pil_image, 'uint8')
            x_train.append(imagearr)
            y_labels.append(id_)

with open("picklejar/face-labels.pickle", 'wb') as f:
    pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels))
recognizer.save("./face-trainner.yml")
