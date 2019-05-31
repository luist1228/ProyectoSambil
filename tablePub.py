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

    #tables = queryNumTables()
    #macAddressList = queryMacAddressStandUp()
    #sitPeople = querySitPeople()

    currentTime = datetime.datetime.now()

    while(True):
        tables = queryNumTables()
        macAddressList = queryMacAddressStandUp()
        sitPeople = querySitPeople()

        if(len(macAddressList) > 0):
            macAddress = macAddressList[int(np.random.uniform(0, len(macAddressList)))]
            macAddressList.remove(macAddress)

            tableID = int(np.random.uniform(0, tables))
            topic = ""

            if(int(np.random.uniform(0,2)) == 1 and len(sitPeople)):
                macAddress = sitPeople[int(np.random.uniform(0, len(sitPeople)))]
                sitPeople.remove(macAddress)
                macAddressList.append(macAddress)
                topic = "Parado"
            else:
                macAddress = macAddressList[int(np.random.uniform(0, len(macAddressList)))]
                macAddressList.remove(macAddress)
                sitPeople.append(macAddress)
                topic = "Sentado"

            payload = {
                "tableID": str(tableID),
                "macAddress": str(macAddress),
                "time": str(currentTime)
            }

            print(payload)
            currentTime = currentTime + datetime.timedelta(hours=1)

            client.publish("Sambil/Mesa/" + topic, json.dumps(payload), qos=0)

        time.sleep(0.5)


def queryMacAddressStandUp():
    macAddressList = []
    macAddressCounter = 0
    while(macAddressCounter < 60):
        macAddress = ""
        counter = 0
        while(counter < 12):
            if(counter%2 != 1 and counter > 0):
                macAddress += ":"

            macAddress += str(random.choice('0123456789ABCDEF'))
            counter += 1

        macAddressList.append(macAddress)
        macAddressCounter += 1

    return macAddressList

def querySitPeople():
    macAddressList = []
    macAddressCounter = 0
    while(macAddressCounter < 0):
        macAddress = ""
        counter = 0
        while(counter < 12):
            if(counter%2 != 1 and counter > 0):
                macAddress += ":"

            macAddress += str(random.choice('0123456789ABCDEF'))
            counter += 1

        macAddressList.append(macAddress)
        macAddressCounter += 1

    return macAddressList

def queryNumTables():
    return 10

if __name__ == "__main__":
    main()
    sys.exit(0)