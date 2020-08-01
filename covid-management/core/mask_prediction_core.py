from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from const import constants
import numpy as np
import cv2


def predict_mask(image, faceModel, maskModel, imgText, outputPath):
	noMask = False
	locList = []

	(h, w) = image.shape[:2]

	# Creating a blob from the frame
	blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300), (104.0, 177.0, 123.0))

	# Detecting faces
	faceModel.setInput(blob)
	faceDetections = faceModel.forward()

	# Iterating detected faces
	for i in range(0, faceDetections.shape[2]):
		# confidence of detection
		confidence = faceDetections[0, 0, i, 2]

		if confidence > constants.FACE_MODEL_CONFIDENCE:
			# Getting coordinates of the bounding box for face detections
			box = faceDetections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# Verifying the validity of coordinates
			(startX, startY) = (max(0, startX), max(0, startY))
			(endX, endY) = (min(w - 1, endX), min(h - 1, endY))
			
			if startX > w-1 or startY > h-1:
				continue
			if endX < 0 or endY < 0:
				continue

			# Get the detected face and do pre-processing
			faceRegion = image[startY:endY, startX:endX]
			faceRegion = cv2.cvtColor(faceRegion, cv2.COLOR_BGR2RGB)
			faceRegion = cv2.resize(faceRegion, (224, 224))
			faceRegion = img_to_array(faceRegion)
			faceRegion = preprocess_input(faceRegion)
			faceRegion = np.expand_dims(faceRegion, axis=0)

			# Check for mask
			(withMask, withoutMask) = maskModel.predict(faceRegion)[0]

			if withoutMask > withMask:
				color = (0, 0, 255)
				noMask = True
				# Draw the bounding box
				cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
				# Add the coordinates to the location list
				locList.append({"startX" :  startX if isinstance(startX, int) else startX.item(), 
					"startY" : startY if isinstance(startY, int) else startY.item(), 
					"endX" : endX if isinstance(endX, int) else endX.item(), 
					"endY" : endY if isinstance(endY, int) else endY.item()})
	
	if noMask:
		# Write the output image
		cv2.putText(image, constants.NOMASK_TEXT, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.85, color, 2)
		cv2.putText(image, imgText, (10, image.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
		cv2.imwrite(outputPath, image)
		cv2.imshow("Output", image)
		cv2.waitKey(1)
	
	return noMask, locList