import ssl
import sys
import json
import random
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish
import numpy as np
import datetime
import psycopg2 as psy
import pandas as pd

conn=psy.connect(host = 'localhost', user= 'postgres', password ='12t09lma', dbname= 'SambilDB')

def contarCamaras():
  #Numero de personas
  sql='''SELECT *  
  FROM public."camara";'''
  df = pd.read_sql_query(sql, conn)
  camaras = df.id.count()
  return camaras

def listaAdentro():
    sql='''select e."macadd" from entradap as e
    left join salidap as s on s."macadd"=e."macadd" 
    where s."id" IS NULL and e."macadd" is not null'''
    df = pd.read_sql_query(sql, conn)

    sql='''select *from salidap as e
    where "macadd" is null'''
    df2 = pd.read_sql_query(sql, conn)

    sql='''select *from entradap as e
    where "macadd" is null'''
    df3 = pd.read_sql_query(sql, conn)

    entro=len(df2["id"])
    salio=len(df3["id"])
    adentro=salio-entro
    

    print(adentro)
    
    Lista = []
    for index, row in df.iterrows():
        Lista.append(row["macadd"])
    
    while adentro > 0 :
        Lista.append("null")
        adentro -= 1

    return Lista

def on_connect():
    print("Pub connected!")

def main():
    client = mqtt.Client("EntrancePub", False)
    client.qos = 0
    client.connect(host="localhost")

    mallAccess =contarCamaras()  #Number of mall access
    currentTime = datetime.datetime.now()
    listaAdentro()
    time.sleep(5)
    macAddress = ""
    macAddressList = listaAdentro()
    print(macAddressList)
    avgEntries = 500
    stdEntries = 50
    entries = np.random.normal(avgEntries, stdEntries)

    while(entries):
        accessID = int(np.random.uniform(1 , mallAccess+1))

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

            client.publish("Sambil/Camaras/Entrada", json.dumps(payload), qos=0)

        else:
            macAddress = macAddressList[int(np.random.uniform(0, len(macAddressList)))]
            macAddressList.remove(macAddress)

            payload = {
                "camaraID": str(accessID),
                "macAddress": str(macAddress),
                "time": str(currentTime)
            }

            client.publish("Sambil/Camaras/Salida", json.dumps(payload), qos=0)

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
