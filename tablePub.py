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

def on_connect():
    print("Pub connected!")

def main():
    client = mqtt.Client("TablePub", False)
    client.qos = 0
    client.connect(host="localhost")

    tables = queryNumTables()
    idMesas()
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
    
    Lista = []
    for index, row in df.iterrows():
        Lista.append(row["macadd"])
    
    while adentro > 0 :
        Lista.append("null")
        adentro -= 1

    return Lista

def querySitPeople():
    macAddressList = []
    
    return macAddressList

def queryNumTables():
    sql='''SELECT *  
    FROM public."mesa";'''
    df = pd.read_sql_query(sql, conn)
    mesas = df.id.count()
    print(mesas)
    return mesas

def idMesas():
    mesaslista=[]
    sql='''select b."id" from beacon as b
    inner join tienda as s on b."id"= s."fkbeacon";'''
    df = pd.read_sql_query(sql, conn)
    for index, row in df.iterrows():
        mesaslista.append(row["id"])
    print(mesaslista)

if __name__ == "__main__":
    main()
    sys.exit(0)
