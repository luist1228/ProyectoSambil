import ssl
import sys
import psycopg2 
import pandas as pd
import paho.mqtt.client 
import json


conn = psycopg2.connect(host = 'localhost', user= 'postgres', password ='12t09lma', dbname= 'SambilDB')

def on_connect(client, userdata, flags, rc):    
    print('Conectado (%s)' % client._client_id)
    client.subscribe(topic='Sambil/#', qos = 0) 


def on_message_C(client,userdata,message): 
    print('------------------------------')
    c= json.loads(message.payload)
    if (message.topic=="Sambil/Camaras/Entrada") :
        if (c["macAddress"]!="null"):
            print(c)
            print('topic: %s' % message.topic)
            cur = conn.cursor()
            sql = '''INSERT INTO public."entradap" (fkcamara, sexo, edad, macadd, registroe)VALUES ( %s, %s, %s, %s, %s);'''
            cur.execute(sql, (c["camaraID"],c["gender"], c["age"],c["macAddress"],c["time"]))
            conn.commit()
        else:
            print(c)
            print('topic: %s' % message.topic)
            cur = conn.cursor()
            sql = '''INSERT INTO public."entradap" (fkcamara, sexo, edad, registroe)VALUES ( %s, %s, %s, %s);'''
            cur.execute(sql, (c["camaraID"],c["gender"], c["age"],c["time"]))
            conn.commit()
    else:
        if (c["macAddress"]!="null"):
            print(c)
            print('topic: %s' % message.topic)
            cur = conn.cursor()
            sql = '''INSERT INTO public."salidap"(fkcamara, registros, macadd)VALUES (%s, %s, %s);'''
            cur.execute(sql, (c["camaraID"],c["time"],c["macAddress"]))
            conn.commit()
        else:
            print(c)
            print('topic: %s' % message.topic)
            cur = conn.cursor()
            sql = '''INSERT INTO public."salidap"(fkcamara, registros)VALUES (%s, %s);'''
            cur.execute(sql, (c["camaraID"],c["time"]))
            conn.commit()


    
def on_message_B(client,userdata,message):   
    b = json.loads(message.payload)
    print('------------------------------')
    print("Beacon")
    print('topic: %s' % message.topic)
    print(b)
    print('qos: %s' % message.qos)

def on_message_S(client,userdata,message):   
    s = json.loads(message.payload)
    print('------------------------------')
    print("Sensor")
    print('topic: %s' % message.topic)
    print(s)
    print('qos: %s' % message.qos)

def main():	
    client = paho.mqtt.client.Client(client_id='Actividad Sambil',clean_session=False)
    client.on_connect = on_connect
    client.message_callback_add('Sambil/Camaras/#', on_message_C)
    client.message_callback_add('Sambil/Beacons/#', on_message_B)
    client.message_callback_add('Sambil/Sensors/#', on_message_S)
    client.connect(host='localhost') 
    client.loop_forever()

if __name__ == '__main__':
	main()
	sys.exit(0)