
from core.people_detection import detect_people
from const import constants as consts
from scipy.spatial import distance as dist
import numpy as np
import argparse
import imutils
import cv2
import os

def detect_social_distancing(frame, minDist, objDetectionModel, LABELS, imgText, crowdTh, outputPathSD, outputPathCrowded):
	sdBreach = False
	crowded = False
	locList = []
	
	layerNames = objDetectionModel.getLayerNames()
	layerNames = [layerNames[i[0] - 1] for i in objDetectionModel.getUnconnectedOutLayers()]

	detections = detect_people(frame, objDetectionModel, layerNames, personIdx=LABELS.index("person"))
	
	if len(detections) > crowdTh:
		crowded = True
		crowdedFrame = frame.copy()

	violations = set()

	# Proceed with further proceesing for at least two detections
	if len(detections) >= 2:
		# Pairwise ditance calculation
		centroids = np.array([r[2] for r in detections])
		D = dist.cdist(centroids, centroids, metric="euclidean")

		for i in range(0, D.shape[0]):
			for j in range(i + 1, D.shape[1]):
				# check for minimum distance violations
				if D[i, j] < minDist:
					violations.add(i)
					violations.add(j)

	# iterate the detections
	for (i, (prob, bbox, centroid)) in enumerate(detections):
		# Get the coordinates of bounding box and centroid
		(startX, startY, endX, endY) = bbox
		(cX, cY) = centroid
		color = (0, 255, 0)

		if i in violations:
			color = (0, 0, 255)
			sdBreach = True
			cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
			locList.append({"startX" :  startX if isinstance(startX, int) else startX.item(), 
					"startY" : startY if isinstance(startY, int) else startY.item(), 
					"endX" : endX if isinstance(endX, int) else endX.item(), 
					"endY" : endY if isinstance(endY, int) else endY.item()})

	if sdBreach :
		cv2.putText(frame, consts.SD_TEXT , (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 2)	
		cv2.putText(frame, imgText, (10, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)	
		cv2.imwrite(outputPathSD, frame)
		cv2.imshow("Output", frame)
		cv2.waitKey(1)
	if crowded :
		cv2.putText(crowdedFrame, "Crowd Count > "+str(crowdTh), (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 0, 255), 2)	
		cv2.putText(crowdedFrame, imgText, (10, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)	
		cv2.imwrite(outputPathCrowded, crowdedFrame)
		cv2.imshow("Output", crowdedFrame)
		cv2.waitKey(1)

	return crowded, sdBreach, locList
