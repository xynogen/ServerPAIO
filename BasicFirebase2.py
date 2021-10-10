import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import json
import time
import requests




cred = credentials.Certificate("./PAIO_AdminSDK.json")
app = firebase_admin.initialize_app(cred)

ref = db.reference("/", app, "https://autofish-d31e9-default-rtdb.asia-southeast1.firebasedatabase.app")

def getSensorData():
    data = None
    
    try:
        data = requests.get("http://192.168.0.100")

    except Exception:
        time.sleep(2)
        getSensorData()

    if (data.content != None):
        return json.loads(data.content)
    else:
        return None


while True:
    data = getSensorData()
    if data != None :
        print(data)
        print("=====================")
        ref.child("data").set(data)
    else:
        pass    

    time.sleep(3.5)

    

    

