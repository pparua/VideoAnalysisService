from const.constants import NMS_THRESH
from const.constants import MIN_CONF
import numpy as np
import cv2

def detect_people(frame, objDetectionModel, layerNames, personIdx=0):
	# Get the dimensions of the frame
	(H, W) = frame.shape[:2]
	results = []

	# passing blob to the object detector for obtaining bounding boxes
	blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
	objDetectionModel.setInput(blob)
	outputs = objDetectionModel.forward(layerNames)

	boxes = []
	centroids = []
	confidences = []

	# iterating outputs
	for output in outputs:
		for detection in output:
			# Get classID & Confidence
			scores = detection[5:]
			classID = np.argmax(scores)
			confidence = scores[classID]

			# Check for person class
			if classID == personIdx and confidence > MIN_CONF:
				box = detection[0:4] * np.array([W, H, W, H])
				(centerX, centerY, width, height) = box.astype("int")

				#  Get the top and left corner of the bounding box
				x = int(centerX - (width / 2))
				y = int(centerY - (height / 2))

				# update bounding box coordinates
				boxes.append([x, y, int(width), int(height)])
				centroids.append((centerX, centerY))
				confidences.append(float(confidence))

	# Apply non-maxima suppression
	idxs = cv2.dnn.NMSBoxes(boxes, confidences, MIN_CONF, NMS_THRESH)

	# Check for at least one detection 
	if len(idxs) > 0:
		for i in idxs.flatten():
			# extract the bounding box coordinates
			(x, y) = (boxes[i][0], boxes[i][1])
			(w, h) = (boxes[i][2], boxes[i][3])
			r = (confidences[i], (x, y, x + w, y + h), centroids[i])
			results.append(r)

	return results