import ssl
import sys
import psycopg2 
import pandas as pd
import paho.mqtt.client 
import json

def on_connect(client, userdata, flags, rc):    
    print('Conectado (%s)' % client._client_id)
    client.subscribe(topic='Sambil/#', qos = 0) 

def on_message_C(client,userdata,message): 
    c= json.loads(message.payload)
    print('------------------------------')
    print("Camara")
    print('topic: %s' % message.topic)
    print(c)
    print('qos: %s' % message.qos)

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