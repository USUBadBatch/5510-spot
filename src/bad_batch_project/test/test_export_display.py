import cv2

KEY_ESC = 27

webcam = cv2.VideoCapture(0)
if not webcam.isOpened():
	raise IOError("Cant open webcam")

while True:
	frame_status, frame = webcam.read()
	cv2.imshow("Spot Webcam feed(ESC to exit)", frame)
	
	key = cv2.waitKey(1)
	if key == KEY_ESC:
		break
webcam.release()
cv2.destroyAllWindows()
