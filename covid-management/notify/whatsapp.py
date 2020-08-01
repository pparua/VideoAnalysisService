from twilio.rest import Client
from const import constants as consts

# Notify Admin via whatsapp
def notifyAdmin(msg, imgName):
	client = Client(consts.SID, consts.AUTH_TOKEN)
	message = client.messages.create(body=msg,
                           media_url=consts.IBM_COS_PUB_URL + imgName,
                           from_=consts.FROM_WHATSAPP_NUMBER,
                           to=consts.TO_WHATSAPP_NUMBER)
	print(message.sid)
	# print(consts.IBM_COS_PUB_URL + imgName)
	print("Breach message sent to Admin via WhatsApp..\n")