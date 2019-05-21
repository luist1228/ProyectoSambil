import sys
import json
import time
import paho.mqtt.client
import paho.mqtt.publish
import numpy as np
import datetime
import pandas as pd
import psycopg2 as psy

conn=psy.connect(host = 'localhost', user= 'postgres', password ='12t09lma', dbname= 'Lab2')

def main():
    client = paho.mqtt.client.Client(client_id='Sensores',clean_session=False)
    client.qos = 0
    client.connect(host='localhost')
    payload = {
        "Mensaje": "Holaaa"
		}
    client.publish('Sambil/Sensores',json.dumps(payload),qos=0)


if __name__ == '__main__':
	main()
	sys.exit(0)