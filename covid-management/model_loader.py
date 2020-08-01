import cv2
import os
from tensorflow.keras.models import load_model
from const import constants


def get_face_model():    
    # load the face detector model
    print("Loading face detector model...\n")
    prototxtPath = os.path.sep.join([constants.MODEL_DIR, constants.FACE_MODEL_DIR, constants.FACE_MODEL_PROTOTXT])
    weightsPath = os.path.sep.join([constants.MODEL_DIR, constants.FACE_MODEL_DIR, constants.FACE_MODEL_WEIGHTS])
    faceModel = cv2.dnn.readNet(prototxtPath, weightsPath)
    return faceModel


def get_mask_model():    
    # load the face mask detector model
    print("Loading face mask detector model...\n")
    maskModelPath = os.path.sep.join([constants.MODEL_DIR, constants.MASK_MODEL_DIR, constants.MASK_MODEL_NAME])
    maskModel = load_model(maskModelPath)
    return maskModel


def get_obj_detection_model():
    # load the object detection model
    print("Loading object detection model...\n")
    # load the COCO class labels for YOLO model
    labelsPath = os.path.sep.join([constants.MODEL_DIR, constants.OBJ_DETECTION_MODEL_DIR, "coco.names"])
    LABELS = open(labelsPath).read().strip().split("\n")
    # paths to the YOLO weights and model configuration
    weightsPath = os.path.sep.join([constants.MODEL_DIR, constants.OBJ_DETECTION_MODEL_DIR, "yolov3.weights"])
    configPath = os.path.sep.join([constants.MODEL_DIR, constants.OBJ_DETECTION_MODEL_DIR, "yolov3.cfg"])
    # load YOLO object detector trained on COCO dataset
    objDetectionModel = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    return objDetectionModel, LABELS
