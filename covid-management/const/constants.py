# Model Constants
MODEL_DIR               = "model"
FACE_MODEL_DIR          = "face_detector"
FACE_MODEL_PROTOTXT     = "deploy.prototxt"
FACE_MODEL_WEIGHTS      = "res10_300x300_ssd_iter_140000.caffemodel"
MASK_MODEL_DIR          = "mask_detector"
MASK_MODEL_NAME         = "mask_detector.model"
OBJ_DETECTION_MODEL_DIR = "object_detector"

FACE_MODEL_CONFIDENCE = 0.5
MIN_DISTANCE          = 50
MIN_CONF              = 0.3
NMS_THRESH            = 0.3

OUTPUT_DIR_NAME      = "output"
MASK_OUTPUT_IMG_NAME = "maskoutput.jpg"
SD_OUTPUT_IMG_NAME   = "sdoutput.jpg"
NOMASK_TEXT          = "Breach - No Mask"
SD_TEXT              = "Breach - Social Distancing"
DOC_TYPE_V           = "Grid Violations"

# Location Config Data
LOC_CONFIG = {
	2000 : "SDB1 Main Entrance", 
	2001 : "SDB2  Front", 
	2002 : "SDB Gate1 Entrance",
	2003 : "Cafeteria Front",
	2100 : "Lane 541 Camera"
	}

# Breach Config Data
BREACH_CONFIG = {
	"mask"    : { "vid" : 10, "vdesc" : "No Mask"},
	"sd"      : { "vid" : 11, "vdesc" : "Social Distancing Violations"},
	"crowded" : { "vid" : 12, "vdesc" : "Crowd Gathering"}
}

# IBM Cloudant DB Config
DB_NAME     = "dbppmmgriddata"
USERNAME    = "XXXXXXXXXXXXXXXXXX"
API_KEY     = "XXXXXXXXXXXXXXXXXX"

# IBM COS Config
IBM_COS_API_KEY      = "XXXXXXXXXXXXXXXXXX"
IBM_COS_SVC_INSTANCE = "XXXXXXXXXXXXXXXXXX"
IBM_COS_AUTH         = "XXXXXXXXXXXXXXXXXX"
IBM_COS_ENDPOINT     = "XXXXXXXXXXXXXXXXXX"
IBM_COS_BUCKET       = "XXXXXXXXXXXXXXXXXX"
IBM_COS_PUB_URL      = "XXXXXXXXXXXXXXXXXX"

# SMS Constants
SMS_URL = "https://XXXXXXXXXXXXXXXXXX"
ALERT_URL = 'https://XXXXXXXXXXXXXXXXXX'

# WHATSAPP Constants
FROM_WHATSAPP_NUMBER = 'whatsapp:XXXXXXXX'
TO_WHATSAPP_NUMBER   = 'whatsapp:XXXXXXXX'
SID                  = 'XXXXXXXXXXXXXXXXXX'
AUTH_TOKEN           = 'XXXXXXXXXXXXXXXXXX'