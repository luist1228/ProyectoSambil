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
    client = mqtt.Client("StorePub", False)
    client.qos = 0
    client.connect(host="localhost")

    stores = queryNumstores()
    macAddressList = queryMacAddressStandUp()
    peopleInside = querypeopleInside()

    currentTime = datetime.datetime.now()

    while(True):
        #stores = queryNumstores()
        #macAddressList = queryMacAddressStandUp()
        #peopleInside = querypeopleInside()

        if(len(macAddressList) > 0):
            storeID = int(np.random.uniform(0, stores)) + 1
            topic = ""

            if(int(np.random.uniform(0,2)) == 1 and len(peopleInside) > 0):
                ran = int(np.random.uniform(0, len(peopleInside)))

                storeUser = [peopleInside[ran][0], peopleInside[ran][1]]
                peopleInside.remove(storeUser)
                macAddressList.append(storeUser)
                topic = "Saliendo"
            else:
                ran = int(np.random.uniform(0, len(macAddressList)))
                storeUser = [macAddressList[ran], storeID]
                macAddressList.remove(storeUser[0])

                peopleInside.append(storeUser)
                topic = "Entrando"

            payload = {
                "storeID": str(storeUser[1]),
                "macAddress": str(storeUser[0]),
                "time": str(currentTime)
            }

            print(topic)
            print(payload)
            currentTime = currentTime + datetime.timedelta(hours=1)

            client.publish("Sambil/Tienda/" + topic, json.dumps(payload), qos=0)

        time.sleep(0.5)


def queryMacAddressStandUp():
    macAddressList = []
    macAddressCounter = 0
    while(macAddressCounter < 60):
        storeUser = ""
        counter = 0
        while(counter < 12):
            if(counter%2 != 1 and counter > 0):
                storeUser += ":"

            storeUser += str(random.choice('0123456789ABCDEF'))
            counter += 1

        macAddressList.append(storeUser)
        macAddressCounter += 1

    return macAddressList

def querypeopleInside():
    macAddressList = []
    macAddressCounter = 0
    while(macAddressCounter < 0):
        storeUser = ""
        counter = 0
        while(counter < 12):
            if(counter%2 != 1 and counter > 0):
                storeUser += ":"

            storeUser += str(random.choice('0123456789ABCDEF'))
            counter += 1

        macAddressList.append(storeUser)
        macAddressCounter += 1

    return macAddressList

def queryNumstores():
    return 30

if __name__ == "__main__":
    main()
    sys.exit(0)