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


    
def on_message_M(client,userdata,message):   
    m = json.loads(message.payload)
    print('------------------------------')
    if (message.topic=="Sambil/Mesa/Parado") :
       if (m["macAddress"]!="null"):
            print(m)
            print('topic: %s' % message.topic)
            cur = conn.cursor()
            sql = '''INSERT INTO public.registrom( mac, fkmesa, fecha, io)VALUES ( %s, %s, %s, %s);'''
            cur.execute(sql, (m["macAddress"],m["tableID"], m["time"], False))
            conn.commit()
        else:
            print(m)
            print('topic: %s' % message.topic)
            cur = conn.cursor()
            sql = '''INSERT INTO public.registrom(fkmesa, fecha, io)VALUES ( %s, %s, %s);'''
            cur.execute(sql, (m["tableID"], m["time"],False))
            conn.commit()
    else:
        if (m["macAddress"]!="null"):
            print(m)
            print('topic: %s' % message.topic)
            cur = conn.cursor()
            sql = '''INSERT INTO public.registrom( mac, fkmesa, fecha, io)VALUES ( %s, %s, %s, %s);'''
            cur.execute(sql, (m["macAddress"],m["tableID"], m["time"], True))
            conn.commit()
        else:
            print(m)
            print('topic: %s' % message.topic)
            cur = conn.cursor()
            sql = '''INSERT INTO public.registrom(fkmesa, fecha, io)VALUES ( %s, %s, %s);'''
            cur.execute(sql, (m["tableID"], m["time"],True))
            conn.commit()

   
def on_message_T(client,userdata,message): 
    t = json.loads(message.payload)
    print('------------------------------')  
    if (message.topic=="Sambil/Tienda/Entrando") :
        if (t["macAddress"]!="null"):
            print(t)
            print('topic: %s' % message.topic)
            cur = conn.cursor()
            sql = '''INSERT INTO public.registrot(mac, fkbeacon, fecha, io)VALUES (%s, %s, %s, %s);'''
            cur.execute(sql, (t["macAddress"],t["beaconID"], t["time"], True))
            conn.commit()
        else:
            print(t)
            print('topic: %s' % message.topic)
            cur = conn.cursor()
            sql = '''INSERT INTO public.registrot(fkbeacon, fecha, io)VALUES ( %s, %s, %s);'''
            cur.execute(sql, (t["beaconID"], t["time"], True))
            conn.commit()
    else if (message.topic=="Sambil/Tienda/Saliendo") :
        if (t["macAddress"]!="null"):
            print(t)
            print('topic: %s' % message.topic)
            cur = conn.cursor()
            sql = '''INSERT INTO public.registrot(mac, fkbeacon, fecha, io)VALUES (%s, %s, %s, %s);'''
            cur.execute(sql, (t["macAddress"],t["beaconID"], t["time"], False))
            conn.commit()
        else:
            print(t)
            print('topic: %s' % message.topic)
            cur = conn.cursor()
            sql = '''INSERT INTO public.registrot(fkbeacon, fecha, io)VALUES ( %s, %s, %s);'''
            cur.execute(sql, (t["beaconID"], t["time"], False))
            conn.commit()
    else:
         if (t["macAddress"]!="null"):
            print(t)
            print('topic: %s' % message.topic)
            cur = conn.cursor()
            sql = '''INSERT INTO public.compra(fktienda, fkpersonamac, fecha, cedula, nombre, apellido, total)VALUES ( %s, %s, %s, %s, %s, %s, %s);'''
            cur.execute(sql, (t["beaconID"],t["macAddress"], t["time"],t["personID"],t["name"],t["lastname"],t["price"]))
            conn.commit()
        else:
            print(t)
            print('topic: %s' % message.topic)
            cur = conn.cursor()
            sql = '''INSERT INTO public.compra(fktienda, fecha, cedula, nombre, apellido, total)VALUES ( %s, %s, %s, %s, %s, %s);'''
            cur.execute(sql, (t["beaconID"],t["time"],t["personID"],t["name"],t["lastname"],t["price"]))
            conn.commit()



def main():	
    client = paho.mqtt.client.Client(client_id='Actividad Sambil',clean_session=False)
    client.on_connect = on_connect
    client.message_callback_add('Sambil/Camaras/#', on_message_C)
    client.message_callback_add('Sambil/Mesa/#', on_message_M)
    client.message_callback_add('Sambil/Tienda/#', on_message_T)
    client.connect(host='localhost') 
    client.loop_forever()

if __name__ == '__main__':
	main()
	sys.exit(0)