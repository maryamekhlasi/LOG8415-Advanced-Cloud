!/usr/bin/python
"""Python module that receives TCP requests."""

import socket
import mysql
import mysql.connector
from configparser import ConfigParser
import os
import time
import random



def readConfig():
    config = ConfigParser()
    # parse existing file
    print(os.path.dirname(os.path.realpath(__file__))+'/cloud.ini')
    print(config.read(os.path.dirname(os.path.realpath(__file__))+'/cloud.ini'))
    return config

def pingTime():
    config = readConfig()
    ip_list = [config.get('MasterServer', 'ip'), config.get('slave_01', 'ip'), config.get('slave_02', 'ip')]
    min = 1000
    min_ping_ip = '127.0.0.1'
    for ip in ip_list:
        start = time.time()
        os.system('ping -c 1 {}'.format(ip))
        duration = time.time() - start
        if duration < min:
            min = duration
            min_ping_ip = ip
    print(str(min_ping_ip))
    return min_ping_ip

def randint():
    config = readConfig()
    number_list = [config.get('slave_01', 'ip'), config.get('slave_02', 'ip')]
    ip = random.choice(number_list)
    return ip
randint()

def selectMethod(ip):
    mydb = mysql.connector.connect(
    host= ip,
    user="servermysql",
    password="secret",
    database="sakila"
    )
    mycursor = mydb.cursor()
    print("connected to db for select")
    sql = "SELECT * FROM actor"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)
def insertMethod(data, ip):
    mydb = mysql.connector.connect(
    host = ip,
    user="servermysql",
    password="secret",
    database="sakila"
    )
    mycursor = mydb.cursor()
    print('from connected user: ' + str(data))
    splited = str(data).split("|")
    for row in splited:
        firstName = str(row).split(";")[0]
        lastName = str(row).split(";")[1]
        print(firstName + lastName)
        sql = "INSERT INTO actor (first_name, last_name) VALUES (%s, %s)"
        val = (firstName, lastName)
        mycursor.execute(sql, val)
        mydb.commit()

def cleandata(data):
    if "SELECT|RANDOM|" in data:
        data = data.replace("SELECT|RANDOM|", "")
    if "SELECT|CUSTOMIZED|" in data:
        data = data.replace("SELECT|CUSTOMIZED|", "")
    if "SELECT|DIRECT|" in data:
        data = data.replace("SELECT|DIRECT|", "")
    if "SELECT|DIRECT|" in data:
        data = data.replace("SELECT|DIRECT|", "")
    if "INSERT|DIRECT|" in data:
        data = data.replace("INSERT|DIRECT|", "")
    data = data.replace("b'", "")
    data = data.replace("|'", "")
    return data

def main():
    """Main."""
    config = readConfig()
    port = int(config.get('Proxy', 'port'))

    s = socket.socket()
    s.bind(('0.0.0.0', port))

    s.listen(1)  # Listen to one connection
    conn, addr = s.accept()
    print('connection from: ' + str(addr))
    while True:
        data = conn.recv(409600)  # Max bytes
        print('Data: ' + str(data))
        if not data:
            break
        config = readConfig()
        if "INSERT" in str(data):
            ip = config.get('MasterServer', 'ip')
            insertMethod(cleandata(str(data)), ip)

        if "SELECT" in str(data):
            if "RANDOM" in str(data):
                ip = randint ()
                selectMethod(ip)

            if "DIRECT" in str(data):
                ip = config.get('MasterServer', 'ip')
                selectMethod(ip)

            if "CUSTOMIZED" in str(data):
                ip = pingTime()
                print("ping time = "+ ip)
                selectMethod(ip)

if __name__ == '__main__':
    main()


