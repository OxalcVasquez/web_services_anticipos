
import firebase_admin
from firebase_admin import credentials, messaging
import os

pathKey = os.path.abspath("serviceAccountKey.json")
cred = credentials.Certificate(pathKey)
firebase_admin.initialize_app(cred)

def sendPush(title, msg, topic, dataObject=None):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=msg
        ),
        data=dataObject,
        topic=topic,
    )
    response = messaging.send(message)
    print('Successfully sent message:', response)