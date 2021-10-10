import firebase_admin
from firebase_admin import credentials 
from firebase_admin import db
import requests
import time



cred = credentials.Certificate("./PAIO_AdminSDK.json")
app = firebase_admin.initialize_app(cred)

ref = db.reference("/", app, "https://autofish-d31e9-default-rtdb.asia-southeast1.firebasedatabase.app")

def setSwitchState(SwitchName: str, State: int):
    listSwitch = ["SW0", "SW1", "SW2"]
    response = ""

    if SwitchName not in listSwitch:
        print("Switch yang dimasukkan tidak ada di list")
        return -1
    if State != 1 and 0:
        print("State yang dimasukkan Salah")
        return -1
    
    try:
        requests.get("http://192.168.0.101/SW/" + SwitchName[2:3] + "/" + str(State))
    except Exception:
        time.sleep(2)
        setSwitchState(SwitchName, State)

    return 0

def groundState():
    switch = {"blower": "0", "pompa": "0"}
    ref.child("switch").set(switch)
    ref.child("restart").set("0")
    setSwitchState("SW0", 1)
    setSwitchState("SW1", 1)
    setSwitchState("SW2", 1)

def restart():
    data = {"distance": "0", "ph": "0", "temp": "0", "turbidity": "0"}
    ref.child("data").set(data)
    groundState()

def sendPakan():
    setSwitchState("SW0", 0)
    setSwitchState("SW1", 0)
    time.sleep(20)

    setSwitchState("SW0", 1)
    time.sleep(15)
    setSwitchState("SW1", 1)
    groundState()

def sendPompa():
    setSwitchState("SW2", 0)
    time.sleep(20)
    setSwitchState("SW2", 1)
    groundState()

def test(Data):
    print(Data.path)
    print(Data.data)
    print(Data.event_type)
    print("-------------------")

    if (Data.path == "/switch"):
        if (Data.data["blower"] == '1'):
            sendPakan()
    elif (Data.path == "/switch/blower"):
        if (Data.data[0] == '1'):
            sendPakan()

    if (Data.path == "/switch"):
        if (Data.data["pompa"] == '1'):
            sendPompa()
    elif (Data.path == "/switch/pompa"):
        if (Data.data[0] == '1'):
            sendPompa()

    elif (Data.path == "/restart"):
        if (Data.data == "1"):
            restart()
            print("Restart init")

groundState()
ref.listen(test)