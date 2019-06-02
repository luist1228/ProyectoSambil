import ssl
import sys
import psycopg2 
import pandas as pd
import paho.mqtt.client 
import json


conn = psycopg2.connect(host = 'localhost', user= 'postgres', password ='12t09lma', dbname= 'SambilDB')

def main():	
    cur = conn.cursor()
    sql = '''INSERT INTO public.registrom( mac, fkmesa, io)VALUES ( %s, %s, %s);'''
    cur.execute(sql, ("lole",1, False))
    conn.commit()


if __name__ == '__main__':
	main()
	sys.exit(0)