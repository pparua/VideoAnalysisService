import argparse
import cv2
import imutils
from db import breach
from const import constants as consts

# Argument Parsing
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--client", required=True, help="Client ID")
ap.add_argument("-p", "--path",   required=True, help="Path to input file")
ap.add_argument("-l", "--loc",    required=True, help="Location ID")
args = vars(ap.parse_args())

filePath   = args["path"]
locId      = int(args["loc"])
clientId   = args["client"]

vs = cv2.VideoCapture(filePath)
i = 0;

# Capture the first rame from video
while True:
	(frame_exists, frame) = vs.read()

	if not frame_exists:
		break
	else:
		frame = imutils.resize(frame, width=700)
	if i == 0:
		cv2.imwrite("layout.jpg", frame)
		break

# Push the config data(First frame for Layout image) to DB
def pushConfigToDB():
    jsonDoc = {
        "clientId": clientId,
        "locId"   : locId,
        "locDesc" : consts.LOC_CONFIG[locId],
        "type"    : "Floor Layout",
        "imgName" : "layout.jpg"
    }
    breach.insert_breach_record(jsonDoc, 'layout.jpg')


pushConfigToDB()