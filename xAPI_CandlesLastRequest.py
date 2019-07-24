import ssl
import socket
import json
import numpy as np
import pandas as pd
from datetime import date
from datetime import datetime
import mysql.connector
import decimal
import datetime

#connecto xAPI server, user credentials that are given to you
HOST, PORT = 'xxxx', 5112
command = b'{"command": "login","arguments": {"userId": xxx,"password": "xxx"}}'

#use socket library to connect via web socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
context = ssl.create_default_context()

wrappedSocket = context.wrap_socket(sock, server_hostname="xxx" )
wrappedSocket.connect((HOST, PORT))
wrappedSocket.settimeout(60.0)
wrappedSocket.write(command)

data = wrappedSocket.read(1024)



while(True):
    time = datetime.datetime.utcnow()- datetime.timedelta(minutes=5)
    unixtime = int((time - datetime.datetime(1970,1,1)).total_seconds())
    print(time)
    unixtime_extract = str(unixtime) + '000'
    
    #lets call a method that retrieves 1 minute candles for us 
    command2 = '{"command": "getChartLastRequest","arguments": {"info": {"period": 1,"start":' +  unixtime_extract + ',"symbol": "GBPUSD"}}}'
    cc = bytes(command2, 'utf-8')
    wrappedSocket.write(cc)
    data = wrappedSocket.read(4096)
    #json format need to be unpacked...
    data_fromjson = json.loads(data)
    ohlc_data = data_fromjson['returnData']['rateInfos']
    
    #default database connection 
    user='xxx' #user name
    password='xxx' #password
    ip='xxx' #host

    #connect to mysql
    mydb = mysql.connector.connect(
      host=ip,
      user=user,
      passwd=password,
      database="xxx"
    )
    db_cursor = mydb.cursor()

    for i in ohlc_data:
        no_digits = len(str(int(i['open'])))
        ctm = i['ctm']
        open = i['open']*(10**-no_digits)
        close = (i['open']+i['close'])*(10**-no_digits)
        low = ((i['open']+i['low'])*(10**-no_digits))
        high = ((i['open']+i['high'])*(10**-no_digits))
        sql_insert_query = """ REPLACE  INTO `OHLC_GBPUSD`( `ctm`, `open`, `low`,`high`,`close`) VALUES (%s,%s,%s,%s,%s)"""
        insert_tuple = (ctm,open,low,high,close)   
        result  = db_cursor.execute(sql_insert_query, insert_tuple)
        mydb.commit()
    mydb.close()
