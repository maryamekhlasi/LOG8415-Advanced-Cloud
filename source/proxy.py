#!/usr/bin/python
"""Python module that receives TCP requests."""

import socket
import mysql
import mysql.connector

host = '0.0.0.0'
port = 5001


def main():
    """Main."""
    s = socket.socket()
    s.bind((host, port))

    s.listen(1)  # Listen to one connection
    conn, addr = s.accept()
    print('connection from: ' + str(addr))

    mydb = mysql.connector.connect(
    host="18.212.34.241",
    user="servermysql",
    password="secret",
    database="sakila"
    )
    mycursor = mydb.cursor()

    while True:
        data = conn.recv(409600)  # Max bytes
        print('Data: ' + str(data))
        if not data:
            break
        print('from connected user: ' + str(data))
        splited = str(data).split("|")
        for row in splited:
            row = row.replace("'", "")
            if row != "bINSERT" and row != "INSERT" and row!= "":
                firstName = str(row).split(";")[0]
                lastName = str(row).split(";")[1]
                print(firstName + lastName)
                sql = "INSERT INTO actor (first_name, last_name) VALUES (%s, %s)"
                val = (firstName, lastName)
                mycursor.execute(sql, val)
                mydb.commit()

if __name__ == '__main__':
    main()
