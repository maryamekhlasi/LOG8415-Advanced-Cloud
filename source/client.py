#!/usr/bin/python
"""Python module that sends TCP requests to AWS instance."""

import socket
import csv
import time
import json
from configparser import ConfigParser
import os




def main():
    config = ConfigParser()

    # parse existing file
    print(os.path.dirname(os.path.realpath(__file__))+'/cloud.ini')
    print(config.read(os.path.dirname(os.path.realpath(__file__))+'/cloud.ini'))

    destination = config.get('Client', 'destination')
    host = config.get(destination, 'ip')
    port = int(config.get(destination, 'port'))

    s = socket.socket()
    s.connect((host, port))
    print("here")

    sendData = "INSERT|"
    with open(os.path.dirname(os.path.realpath(__file__)) + '/data/data_dump.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row) 
            sendData = sendData + row[0] + ";" + row[1] + "|"
            s.send(str.encode(sendData))                    
            time.sleep(0.1)
    #s.send(str.encode("hello server!"))
    msg = s.recv(1024)
    print(msg)
    s.close()


if __name__ == '__main__':
    main()
