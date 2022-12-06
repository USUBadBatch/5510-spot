import os
from termcolor import colored
import time
import warnings

warnings.simplefilter(action="ignore", category=UserWarning)
warnings.simplefilter(action="ignore", category=RuntimeWarning)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # or any {'0', '1', '2'}
# Level | Level for Humans | Level Description                  
#  -------|------------------|------------------------------------ 
#   0     | DEBUG            | [Default] Print all messages       
#   1     | INFO             | Filter out INFO messages           
#   2     | WARNING          | Filter out INFO & WARNING messages 
#   3     | ERROR            | Filter out all messages      

f = open(f'{os.getcwd()}/hand-gesture-recognition-code-tensorflow/gesture.names', 'r')
classNames = f.read().split('\n')
if not "config.py" in os.listdir(os.getcwd()):
    with open("config.py", mode="w+") as config:
        data = "config = {\n"
        for name in classNames:
            data += format("\t\"" + name + "\"","15s") + ": [None, {}],\n"
        data += "}"
        config.write(data)
    print(colored("No existing config file found. One has been created for you", "blue"))
    exit()

from config import config


import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf

from utils import spot

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

print(colored("[INFO] Mediapipe hands initialized", "green"))

# Load the gesture recognizer model

print(f"cwd: {os.getcwd()}")
model = tf.keras.models.load_model(f'{os.getcwd()}/hand-gesture-recognition-code-tensorflow/mp_hand_gesture')
print(colored("[INFO] Hands detection model initialized", "green"))

# Load class names



# Initialize the webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError(colored("Unable to open webcam", "red"))
print(colored("[INFO] Webcam initialized", "green"))
spot.init()
print(colored("[INFO] Spot initialized", "green"))

predictions = {}
while True:
    # Read each frame from the webcam
    time.sleep(.1)
    
    _, frame = cap.read()

    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    # print(result)
    
    className = ''

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                # print(id, lm)
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)

                landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            # mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            # Predict gesture
            prediction = model([landmarks])
            # print(prediction)
            classID = np.argmax(prediction)
            className = classNames[classID]

            if predictions.get(className, None) is not None:
                predictions[className] += 1
            else:
                if config[className][0] is not None:
                    predictions.update({className : 1})

            print(className)
            print(predictions)

            if len(predictions) > 0:
                print(max(list(predictions.values())))
                max_count = max(list(predictions.values()))
                if max_count > 10:
                    hand_shape = list(predictions.keys())[list(predictions.values()).index(max_count)]
                    if (config[hand_shape][0] is not None):
                        predictions = {}
                        kwargs = config[hand_shape][1]
                        config[hand_shape][0](**kwargs)


    # show the prediction on the frame
    # cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                #    1, (0,0,255), 2, cv2.LINE_AA)

    # Show the final output
    # cv2.imshow("Output", frame) 

    if cv2.waitKey(1) == ord('q'):
        break

# release the webcam and destroy all active windows
cap.release()

cv2.destroyAllWindows()