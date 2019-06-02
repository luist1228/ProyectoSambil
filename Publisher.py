import ssl
import sys
import json
import random
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish
import numpy as np
import datetime

knownPeople = []
peopleInside = []
peopleSitting = []
peopleInStore = []

def on_connect():
    print("Pub connected!")

def main():
    client = mqtt.Client("Publisher", False)
    client.qos = 0
    client.connect(host="localhost")

    #Database variables
    numAccess = queryNumAccess()
    storeBeaconID = queryStoreBeaconID()
    tableBeaconID = queryTableBeaconID()
    currentTime = datetime.datetime.now().replace(hour=8, minute=0)

    days = 31

    while(days > 0):
        print(currentTime)
        visits = getNumVisits()
        while(visits > 0 and currentTime.hour < 22):
            if(int(np.random.uniform(0,2)) != 0):
                pubEntrance(client,numAccess,currentTime)
                currentTime = currentTime + datetime.timedelta(minutes=1)
                visits -= 1
            if(int(np.random.uniform(0,3)) == 0):
                pubStores(client,storeBeaconID,currentTime)
            if(int(np.random.uniform(0,3)) == 0):
                pubTables(client,tableBeaconID,currentTime)
                currentTime = currentTime + datetime.timedelta(minutes=1)

            currentTime = currentTime + datetime.timedelta(minutes=6)


        print("\nStart Closing the C.C.")
        while((len(peopleInside) + len(peopleInStore) + len(peopleSitting)) > 0):

            ran = np.random.uniform(0, len(peopleInside))
            while(ran > 0):
                cameraID = int(np.random.uniform(0 , numAccess)) + 1
                macAddress = peopleInside[int(np.random.uniform(0, len(peopleInside)))]
                peopleInside.remove(macAddress)

                payload = {
                    "camaraID": str(cameraID),
                    "macAddress": str(macAddress),
                    "time": str(currentTime)
                }
                
                client.publish("Sambil/Camaras/Salida", json.dumps(payload), qos=0)
                print("Saliendo  (C.C.)   --> ", end='')
                print(payload)
                ran -= 1

            ran = np.random.uniform(0, len(peopleSitting))
            while(ran > 0):
                tableUser = random.choice(peopleSitting)
                peopleSitting.remove(tableUser)
                peopleInside.append(tableUser[0])

                payload = {
                    "tableID": str(tableUser[1]),
                    "macAddress": str(tableUser[0][0]),
                    "time": str(currentTime)
                }

                client.publish("Sambil/Mesa/Parado", json.dumps(payload), qos=0)
                print("Parado  (Mesa)   --> ", end='')
                print(payload)
                ran -= 1

            ran = np.random.uniform(0, len(peopleInStore))
            while(ran > 0):
                storeUser = random.choice(peopleInStore)

                #Possible sale before getting out
                pubSales(client, storeUser, currentTime)

                peopleInStore.remove(storeUser)
                peopleInside.append(storeUser[0])

                payload = {
                    "beaconID": str(storeUser[1]),
                    "macAddress": str(storeUser[0][0]),
                    "time": str(currentTime)
                }

                currentTime += datetime.timedelta(minutes=5)

                if(storeUser[0] != "null"): #Beacons only detect users with smartphones
                    client.publish("Sambil/Tienda/Saliendo", json.dumps(payload), qos=0)
                
                print("Saliendo  (Tienda)   --> ", end='')
                print(payload)
                ran -= 1

        print("----------------------------------------------------End of the Simulation------------------------------------------------------------------")
        days -= 1
        currentTime = datetime.timedelta(days=1) +  currentTime.replace(hour=8, minute=0)
        print(currentTime,'fin del dia')


#Publisher's Methods
def pubEntrance(client, numAccess, currentTime):
    macAddress = ""
    topic = ""
    cameraID = int(np.random.uniform(0 , numAccess)) + 1

    if((int(np.random.uniform(0,3)) != 1) or (len(peopleInside) == 0)):
        inside = True
        
        if(int(np.random.uniform(0,5)) == 1 and len(knownPeople) > 0): #if you know the person
            person = random.choice(knownPeople)
            counter = 0
            inside = False

            while(counter < len(peopleInside) or counter < len(peopleInStore) or counter < len(peopleSitting)):
                if(counter < len(peopleInside)):
                    if(person[0] == peopleInside[counter][0]):
                        inside = True
                        break

                if(counter < len(peopleInStore)):
                    if(person[0] == peopleInStore[counter][0][0]):
                        inside = True
                        break

                if(counter < len(peopleSitting)):
                    if(person[0] == peopleSitting[counter][0][0]):
                        inside = True
                        break
                counter += 1
            
            
            if(not inside):
                payload = {
                    "cameraID": str(cameraID),
                    "gender": str(person[1]),
                    "age": str(person[2]),
                    "macAddress": str(person[0]),
                    "time": str(currentTime)
                }
                peopleInside.append(person)

                topic = "Entrada"

        if(inside):
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
                "cameraID": str(cameraID),
                "gender": str(gender),
                "age": str(age),
                "macAddress": str(macAddress),
                "time": str(currentTime)
            }
            
            person = [macAddress,gender,age]

            peopleInside.append(person)

            if(macAddress != "null"):
                knownPeople.append(person)

            topic = "Entrada"

    else:
        macAddress = peopleInside[int(np.random.uniform(0, len(peopleInside)))]
        peopleInside.remove(macAddress)

        payload = {
            "camaraID": str(cameraID),
            "macAddress": str(macAddress),
            "time": str(currentTime)
        }
        topic = "Salida"

    print(topic + "  (C.C.)   --> ", end='')
    print(payload)
    client.publish("Sambil/Camaras/" + topic, json.dumps(payload), qos=0)

def pubStores(client, storeBeaconID, currentTime):
    if(len(peopleInside) > 0):
        beaconID = random.choice(storeBeaconID)
        topic = ""

        if(int(np.random.uniform(0,3)) == 1 and len(peopleInStore) > 0): #Get someone out of store
            storeUser = random.choice(peopleInStore)

            #Possible sale before getting out
            pubSales(client, storeUser, currentTime)

            peopleInStore.remove(storeUser)
            peopleInside.append(storeUser[0])
            topic = "Saliendo"

        else: #Get someone in
            ran = int(np.random.uniform(0, len(peopleInside)))
            storeUser = [peopleInside[ran], beaconID]
            peopleInside.remove(storeUser[0])

            peopleInStore.append(storeUser)
            topic = "Entrando"
        
        payload = {
            "beaconID": str(storeUser[1]),
            "macAddress": str(storeUser[0][0]),
            "time": str(currentTime)
        }

        if(storeUser[0] != "null"): #Beacons only detect users with smartphones
            client.publish("Sambil/Tienda/" + topic, json.dumps(payload), qos=0)

        print(topic + " (Tienda) --> ", end='')
        print(payload)

def pubTables(client, tableBeaconID, currentTime):
    if(len(peopleInside) > 0):
        beaconID = random.choice(tableBeaconID)
        topic = ""

        if(int(np.random.uniform(0,3)) == 1 and len(peopleSitting) > 0):
            tableUser = random.choice(peopleSitting)
            peopleSitting.remove(tableUser)
            peopleInside.append(tableUser[0])
            topic = "Parado"
        else:
            ran = int(np.random.uniform(0, len(peopleInside)))
            tableUser = [peopleInside[ran], beaconID]
            peopleInside.remove(tableUser[0])

            peopleSitting.append(tableUser)
            topic = "Sentado"

        payload = {
            "tableID": str(tableUser[1]),
            "macAddress": str(tableUser[0][0]),
            "time": str(currentTime)
        }

        print(topic + "   (Mesa)   --> ", end='')
        print(payload)

        client.publish("Sambil/Mesa/" + topic, json.dumps(payload), qos=0)

def pubSales(client, buyer, currentTime):
    if(int(np.random.uniform(0,1)) == 0):
        avgPrice = 150
        stdPrice = 100

        price = round(np.random.normal(avgPrice, stdPrice),2)
        while(price <= 0):
            price = round(np.random.normal(avgPrice, stdPrice),2)

        
        if(len(buyer[0])==3):
            correctData = False
            while(not correctData):
                personData = random.choice(dataPeople)
                if(buyer[0][1] == personData["gender"]):
                    correctData = True
                    age = buyer[0][2]
                    if(age > 70):
                        personID = int(np.random.uniform(6000000,600000))
                    elif(age <= 70 and age >= 41):
                        personID = int(np.random.uniform(14000000,6000000))
                    elif(age <= 40 and age >= 26):
                        personID = int(np.random.uniform(22000000,15000000))
                    elif(age <= 25 and age >= 17):
                        personID = int(np.random.uniform(28000000,22000000))      
                    elif(age <= 16 and age >= 8):
                        personID = int(np.random.uniform(36000000,28000000))
                    else:
                        personID = "null"
            name = personData["first_name"]
            lastname = personData["last_name"]
        else:
            personID = buyer[0][3]
            name = buyer[0][4]
            lastname = buyer[0][5]

        #Case for random ID (trigger asqueroso de Nicolas)
        if(np.random.uniform(0,5) == 0):
            randomPerson = random.choice(knownPeople)
            counter = 0
            inside = False
            while(counter < len(peopleInside)):
                if(randomPerson[0] == peopleInside[counter][0]):
                    inside = True
            if(len(randomPerson) > 3 and (not inside)):
                personID = randomPerson[3]

        payload = {
            "beaconID": str(buyer[1]),
            "macAddress": str(buyer[0][0]),
            "name": str(name),
            "lastname": str(lastname),
            "personID": str(personID),
            "time": str(currentTime),
            "price": str(price)
        }

        if(buyer[0] != "null" and len(buyer[0]) ==3):
            counter = 0
            while(counter < len(knownPeople)):
                if(buyer[0][0] == knownPeople[counter][0]):
                    knownPeople[counter].append(personID)
                    knownPeople[counter].append(name)
                    knownPeople[counter].append(lastname)
                    break
                counter += 1

        print("Compra   (Tienda)   --> ", end='')
        print(payload)

        client.publish("Sambil/Tienda/Compra", json.dumps(payload), qos=0)


#Logical Funtions
def getMacAddress():
    macAddress = ""
    counter = 0
    while(counter < 12):
        if(counter%2 != 1 and counter > 0):
            macAddress += ":"

        macAddress += str(random.choice('0123456789ABCDEF'))
        counter += 1

    return macAddress

def getNumVisits():
    avgEntries = 500
    stdEntries = 50
    return np.random.normal(avgEntries, stdEntries)

def getJsonData():
    with open('database.json') as json_file:  
        data = json.load(json_file)
        
    return data['nombres']

dataPeople = getJsonData()

#Query Funtions
def queryNumAccess():
    return 3

def queryStoreBeaconID():
    return [2,4,6,8,10,12,14,16]

def queryTableBeaconID():
    return [1,3,5,7,9,11,13,15]


if __name__ == "__main__":
