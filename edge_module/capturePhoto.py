import cv2
from datetime import datetime
import os
import numpy as np


def capture(gray):
	cap = cv2.VideoCapture(0)
	ret, frame = cap.read()
	if gray:
		frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		grayscale = True
	else:
		grayscale = False
		pass
	date_time = datetime.today()
	filename = 'photos/capture'+str(date_time)+'.jpg'
	out = cv2.imwrite(filename, frame)
	cap.release()
	cv2.destroyAllWindows()
	return filename, date_time, grayscale