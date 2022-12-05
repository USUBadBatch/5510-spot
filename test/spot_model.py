import cv2
import numpy as np
import mediapipe as mp
import tensorflow as tf
import os

import bosdyn.client
from bosdyn.client.image import ImageClient
from bosdyn.client.robot_command import RobotCommandClient, blocking_stand
from PIL import Image
import io
from bosdyn.geometry import EulerZXY
from bosdyn.client.robot_command import RobotCommandBuilder
from utils.auth import get_spot_password, get_spot_username

mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognizer model

print(f"cwd: {os.getcwd()}")
model = tf.keras.models.load_model(f'{os.getcwd()}/hand-gesture-recognition-code-tensorflow/mp_hand_gesture')

# Load class names
f = open(f'{os.getcwd()}/hand-gesture-recognition-code-tensorflow/gesture.names', 'r')
classNames = f.read().split('\n')
f.close()
print(classNames)



sdk = bosdyn.client.create_standard_sdk('understanding-spot')
robot = sdk.create_robot('192.168.80.3')
id_client = robot.ensure_client('robot-id')
print(id_client.get_id())

robot.authenticate(get_spot_username(), get_spot_password())
state_client = robot.ensure_client('robot-state')
print(state_client.get_robot_state())


image_client = robot.ensure_client(ImageClient.default_service_name)
sources = image_client.list_image_sources()
print([source.name for source in sources])


estop_client = robot.ensure_client('estop')
print(estop_client.get_status())

estop_endpoint = bosdyn.client.estop.EstopEndpoint(client=estop_client, name='my_estop', estop_timeout=9.0)
estop_endpoint.force_simple_setup()

print(estop_client.get_status())

estop_keep_alive = bosdyn.client.estop.EstopKeepAlive(estop_endpoint)
print(estop_client.get_status())

lease_client = robot.ensure_client('lease')
print(lease_client.list_leases())

lease = lease_client.take()
lease_keep_alive = bosdyn.client.lease.LeaseKeepAlive(lease_client)
print(lease_client.list_leases())

robot.power_on(timeout_sec=20)
print(f"Power Status: {robot.is_powered_on()}")

robot.time_sync.wait_for_sync()

command_client = robot.ensure_client(RobotCommandClient.default_service_name)
blocking_stand(command_client, timeout_sec=10)

while (1):
    image_response = image_client.get_image_from_sources(["back_fisheye_image"])[0]
    image = Image.open(io.BytesIO(image_response.shot.image.data)).convert("RGB")

    image = np.array(image)

    x, y, z = image.shape
    # print(f"shape: {image.shape}")

    # image = image.reshape(x, y)
    # print(f"shape: {image.shape}")
    # image = np.dstack((image,image,image)).astype(np.uint8)
    # print(f"shape: {image.shape}")
    # print(f"dtype: {image.dtype}")
    # frame = cv2.flip(image, 1)
    # image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    
    # Get hand landmark prediction
    result = hands.process(image)

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
            mpDraw.draw_landmarks(image, handslms, mpHands.HAND_CONNECTIONS)

            # Predict gesture
            prediction = model.predict([landmarks])
            # print(prediction)
            classID = np.argmax(prediction)
            className = classNames[classID]

    # show the prediction on the frame
    cv2.putText(image, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                   1, (0,0,255), 2, cv2.LINE_AA)

    # Show the final output
    cv2.imshow("Output", image) 

    if cv2.waitKey(1) == ord('q'):
        break



cv2.destroyAllWindows()



# Command Spot to rotate about the Z axis.
footprint_R_body = EulerZXY(yaw=0.4, roll=0.0, pitch=0.0)
cmd = RobotCommandBuilder.synchro_stand_command(footprint_R_body=footprint_R_body)
command_client.robot_command(cmd)
cmd = RobotCommandBuilder.synchro_stand_command(body_height=0.1)
command_client.robot_command(cmd)

robot.power_off(cut_immediately=False)




# Initialize the webcam
# cap = cv2.VideoCapture(0)

# while True:
#     # Read each frame from the webcam
#     _, frame = cap.read()

#     x, y, c = frame.shape

#     # Flip the frame vertically
#     frame = cv2.flip(frame, 1)
#     framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Get hand landmark prediction
#     result = hands.process(framergb)

#     # print(result)
    
#     className = ''

#     # post process the result
#     if result.multi_hand_landmarks:
#         landmarks = []
#         for handslms in result.multi_hand_landmarks:
#             for lm in handslms.landmark:
#                 # print(id, lm)
#                 lmx = int(lm.x * x)
#                 lmy = int(lm.y * y)

#                 landmarks.append([lmx, lmy])

#             # Drawing landmarks on frames
#             mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

#             # Predict gesture
#             prediction = model.predict([landmarks])
#             # print(prediction)
#             classID = np.argmax(prediction)
#             className = classNames[classID]

#     # show the prediction on the frame
#     cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
#                    1, (0,0,255), 2, cv2.LINE_AA)

#     # Show the final output
#     cv2.imshow("Output", frame) 

#     if cv2.waitKey(1) == ord('q'):
#         break

# # release the webcam and destroy all active windows
# cap.release()

# cv2.destroyAllWindows()