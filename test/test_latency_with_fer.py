# import fer
import cv2
import os
from fer import utils
import fer

KEY_ESC = 27

webcam = cv2.VideoCapture(0)
if not webcam.isOpened():
    raise IOError("Cant open webcam")

detector = fer.FER()
while True:
    frame_status, frame = webcam.read()
    faces = detector.detect_emotions(frame)
    # frame = utils.draw_annotations(frame, faces, boxes=True, scores=True)

    # cv2.imshow("Spot Webcam Feed(ESC to exit)", frame)

    if faces != []:
        print(faces)

    key = cv2.waitKey(1)
    if key == KEY_ESC:
        break

webcam.release()
cv2.destroyAllWindows()