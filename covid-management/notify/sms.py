import requests
from const import constants as consts

# Notify Admin via text message
def notifyAdmin(locId, msg, imgName):   
    notifyURL = consts.SMS_URL
    ploads = {'locationCd' : str(locId),'messageToSend': msg + ' ' + consts.IBM_COS_PUB_URL + imgName, 'sendFlag':'Y'}
    res = requests.get(notifyURL, params=ploads)
    print(res.text)
    #print(res.url) 
    print("\n")

