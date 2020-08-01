import time
import argparse
import imutils
import cv2
import os
import model_loader
from datetime import datetime
from imutils.video import VideoStream
from core  import mask_prediction_core
from core  import sd_detection_core
from const import constants as consts
from db import breach
from notify import sms
from notify import whatsapp


# Argument Parsing
ap = argparse.ArgumentParser()
ap.add_argument("-b", "--breach", default='all', help="Breach Type : mask/sd/crowded")
ap.add_argument("-i", "--input",  default='video', help="Input file type : image/video")
ap.add_argument("-p", "--path",   required=True, help="Path to input file")
ap.add_argument("-c", "--client", required=True, help="Client ID")
ap.add_argument("-l", "--loc",    required=True, help="Location ID")
ap.add_argument("-n", "--notify", default='sms', help="Notify to Admin : sms/wapp/no")
ap.add_argument("-f", "--fpr",    default=25,    help="Frame Processing rate")
ap.add_argument("-d", "--density", default=20,   help="Crowd threashold")
ap.add_argument("-m", "--min",     default=50,   help="Safe distance")

args = vars(ap.parse_args())

inputType  = args["input"]
breachType = args["breach"].split(",")
filePath   = args["path"]
clientId   = args["client"]
locId      = int(args["loc"])
locDesc    = consts.LOC_CONFIG[locId]
notify    =  args["notify"]
fpr        = int(args["fpr"])
cwowdTh    = int(args["density"])
minDist	   = int(args["min"])

# Model Loading
faceModel = model_loader.get_face_model()
maskModel = model_loader.get_mask_model()
objDetectionModel, LABELS = model_loader.get_obj_detection_model()


# Notify Admin regarding breach
def notifyBreach(msg, imgName):
	if notify  == 'sms':
		sms.notifyAdmin(locId, msg, imgName)
	elif notify == 'wapp':
		whatsapp.notifyAdmin(msg, imgName)


# Detect breach from input frame
def detect_breach(frame, vTime, strTime, imgText, prefix):
	orig = frame.copy()
	
	# Checking for No-mask breach
	if 'mask' in breachType or 'all' in breachType :
		noMask, locList = mask_prediction_core.predict_mask(frame, faceModel, maskModel, 
			imgText, os.path.sep.join([consts.OUTPUT_DIR_NAME, prefix+'mask.jpg']))	
		if noMask:
			print("No Mask Breach..\n")
			# Storing data in DB
			breach.pushToDB(clientId, locId, locDesc, locList, vTime, "mask", 
				strTime, prefix+'mask.jpg')
			notifyBreach("No Mask Breach at " + locDesc, str(vTime) + 'mask' +'.jpg')
	
	# Checking for Social Distancing/Crowed Loc breach
	if 'sd' in breachType or 'crowded' in breachType or 'all' in breachType:
		crowded, sdBreach, locList = sd_detection_core.detect_social_distancing(orig, minDist, 
			objDetectionModel, LABELS, imgText, cwowdTh, 
			os.path.sep.join([consts.OUTPUT_DIR_NAME, prefix+'sd.jpg']), 
			os.path.sep.join([consts.OUTPUT_DIR_NAME, prefix+'crowd.jpg']))
		if sdBreach and ('sd' in breachType or 'all' in breachType):
			print("Social Distancing Breach..\n")
			# Storing data in DB
			breach.pushToDB(clientId, locId, locDesc, locList, vTime, "sd", strTime, prefix+'sd.jpg')	
			notifyBreach("Social Distancing Breach at " + locDesc, str(vTime) + 'sd' +'.jpg')	
		if crowded and ('crowded' in breachType or 'all' in breachType):	
			print("Crowd Gathering more than threashold..\n")
			breach.pushToDB(clientId, locId, locDesc, locList, vTime, "crowded", 
				strTime, prefix+'crowd.jpg')
			notifyBreach("Crowd Gathering Breach at" + locDesc, str(vTime) + 'crowded' +'.jpg')


# Process input video/stream/image and generate frame for breach detection
def process_input():	
	if inputType == 'video':
		print("Starting video stream...\n")
		vs = cv2.VideoCapture(filePath)
		i = 0
		# Iterate over the frames from the video stream
		while True:
			(frame_exists, frame) = vs.read()
		
			if not frame_exists:
				break
			else:
				vTime = int(round(time.time() * 1000))
				strTime = (datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
				imgText = locDesc + ", " + (datetime.now().strftime("%b-%d-%Y %H:%M"))
				frame = imutils.resize(frame, width=700)	
				if i % fpr == 0:
					detect_breach(frame, vTime, strTime, imgText, str(i))
				i = i+1
				
			key = cv2.waitKey(1) & 0xFF
			
			if key == ord("q"):
				break
		cv2.destroyAllWindows()

	elif inputType == 'image':
		vTime = int(round(time.time() * 1000))
		strTime = (datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
		imgText = locDesc + ", " + (datetime.now().strftime("%b-%d-%Y %H:%M"))
		image = cv2.imread(filePath)
		orig = image.copy()
		detect_breach(image, vTime, strTime, imgText, '')
		cv2.waitKey(0)

# Process Input call
process_input()