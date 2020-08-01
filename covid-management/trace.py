import requests
import argparse
from const import constants as consts

def sendAlert(locId):   
    alertURL = consts.ALERT_URL
    ploads = {'locationId' : locId}
    res = requests.get(alertURL, params=ploads)
    print(res.text) 
    # print(res.url)
    print("\n")


# Argument Parsing
ap = argparse.ArgumentParser()
ap.add_argument("-l", "--loc",    required=True, help="Location ID")
args = vars(ap.parse_args())
locId  = args["loc"]
sendAlert(locId)