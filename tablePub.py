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
    client = mqtt.Client("TablePub", False)
    client.qos = 0
    client.connect(host="localhost")

    tables = queryNumTables()
    macAddressList = queryMacAddressStandUp()
    sitPeople = querySitPeople()

    currentTime = datetime.datetime.now()

    while(True):
        #tables = queryNumTables()
        #macAddressList = queryMacAddressStandUp()
        #sitPeople = querySitPeople()

        if(len(macAddressList) > 0):
            tableID = int(np.random.uniform(0, tables)) + 1
            topic = ""

            if(int(np.random.uniform(0,2)) == 1 and len(sitPeople) > 0):
                ran = int(np.random.uniform(0, len(sitPeople)))
                
                tableUser = [sitPeople[ran][0], sitPeople[ran][1]]
                sitPeople.remove(tableUser)
                macAddressList.append(tableUser)
                topic = "Parado"
            else:
                ran = int(np.random.uniform(0, len(macAddressList)))
                tableUser = [macAddressList[ran], tableID]
                macAddressList.remove(tableUser[0])

                sitPeople.append(tableUser)
                topic = "Sentado"

            payload = {
                "tableID": str(tableUser[1]),
                "macAddress": str(tableUser[0]),
                "time": str(currentTime)
            }

            print(topic)
            print(payload)
            currentTime = currentTime + datetime.timedelta(hours=1)

            client.publish("Sambil/Mesa/" + topic, json.dumps(payload), qos=0)

        time.sleep(0.5)


def queryMacAddressStandUp():
    macAddressList = []
    macAddressCounter = 0
    while(macAddressCounter < 60):
        tableUser = ""
        counter = 0
        while(counter < 12):
            if(counter%2 != 1 and counter > 0):
                tableUser += ":"

            tableUser += str(random.choice('0123456789ABCDEF'))
            counter += 1

        macAddressList.append(tableUser)
        macAddressCounter += 1

    return macAddressList

def querySitPeople():
    macAddressList = []
    macAddressCounter = 0
    while(macAddressCounter < 0):
        tableUser = ""
        counter = 0
        while(counter < 12):
            if(counter%2 != 1 and counter > 0):
                tableUser += ":"

            tableUser += str(random.choice('0123456789ABCDEF'))
            counter += 1

        macAddressList.append(tableUser)
        macAddressCounter += 1

    return macAddressList

def queryNumTables():
    return 10

if __name__ == "__main__":
    main()
    sys.exit(0)
