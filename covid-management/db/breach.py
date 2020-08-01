import os
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
from const import constants as consts
from db import cos_upload

# Push JSON Data & Image to Cloudant
def insert_breach_record(jsonDoc, imgPath):
    # create a Cloudant client
    client = Cloudant.iam(consts.USERNAME, consts.API_KEY)

    # Connect to the server
    client.connect()

    # Create an instance of the database
    breachDb = client[consts.DB_NAME]

    # Create a new document
    newDoc = breachDb.create_document(jsonDoc)

    # Verify that the document exists in db
    if newDoc.exists():
        print("Breach data uploaded to server successfully..\n")

    imgData = None
    with open(imgPath, 'rb') as f:
        imgData = f.read()
        resp = newDoc.put_attachment(jsonDoc["imgName"], 'image/jpeg', imgData)

    # print("Attachment successfully added..\n")

    # Disconnect from the server
    client.disconnect()


# Push Breach Details to Cloudant & breach snap to cloud object storage
def pushToDB(clientId, locId, locDesc, locList, vTime, breachType, strTime, outputImgName):
    docType = consts.DOC_TYPE_V
    if breachType == "crowded":
        docType = "Crowd Gathering"
    
    jsonDoc = {
        "clientId": clientId,
        "locId"   : locId,
        "locDesc" : locDesc,
        "type"    : docType,
        "vId"     : consts.BREACH_CONFIG[breachType]["vid"],
        "vDesc"   : consts.BREACH_CONFIG[breachType]["vdesc"],
        "vCoord"  : locList,
        "vTime"   : vTime,
        "strTime" : strTime,
        "imgName" : str(vTime) + breachType +'.jpg'
    }
    
    # Upload data to cloudant
    insert_breach_record(jsonDoc, os.path.sep.join([consts.OUTPUT_DIR_NAME, outputImgName]))
    
    # Upload image to cloud object storage
    cos_upload.upload_file_cos(os.path.sep.join([consts.OUTPUT_DIR_NAME, outputImgName]), jsonDoc["imgName"])
    print("Captured Frame uploaded to server successfully..\n")