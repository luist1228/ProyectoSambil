import ssl
import sys
import json
import random
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish
import numpy as np
import datetime

def on_connect():
    print("Pub connected!")

def main():
    client = mqtt.Client("EntrancePub", False)
    client.qos = 0
    client.connect(host="localhost")

    mallAccess = 3 #Number of mall access
    currentTime = datetime.datetime.now()

    macAddress = ""
    macAddressList = []

    avgEntries = 500
    stdEntries = 50
    entries = np.random.normal(avgEntries, stdEntries)

    while(entries):
        accessID = int(np.random.uniform(0 , mallAccess))

        if((int(np.random.uniform(0,3)) != 1) or (len(macAddressList) == 0)):
            gender = int(np.random.uniform(0,2))

            if(gender == 1):
                gender = "M"
            else:
                gender = "F"

            age = int(np.random.normal(35,15))
            while(age < 9):
                age = int(np.random.normal(35,15))

            if(int(np.random.uniform(0,4)) != 1):
                macAddress = str(getMacAddress())
            else:
                macAddress = "null"

            payload = {
                "camaraID": str(accessID),
                "gender": str(gender),
                "age": str(age),
                "macAddress": str(macAddress),
                "time": str(currentTime)
            }

            macAddressList.append(macAddress)

            client.publish("sambil/camaras/entrada", json.dumps(payload), qos=0)

        else:
            macAddress = macAddressList[int(np.random.uniform(0, len(macAddressList)))]
            macAddressList.remove(macAddress)

            payload = {
                "camaraID": str(accessID),
                "macAddress": str(macAddress),
                "time": str(currentTime)
            }

            client.publish("sambil/camaras/salida", json.dumps(payload), qos=0)

        currentTime = currentTime + datetime.timedelta(hours=1)

        print(payload)
        entries -= 1
        time.sleep(0.5)

def getMacAddress():
    macAddress = ""
    counter = 0
    while(counter < 12):
        if(counter%2 != 1 and counter > 0):
            macAddress += ":"

        macAddress += str(random.choice('0123456789ABCDEF'))
        counter += 1

    return macAddress

if __name__ == "__main__":
    main()
    sys.exit(0)
