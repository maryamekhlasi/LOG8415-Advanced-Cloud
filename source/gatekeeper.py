import re
import os


postValidator = re.compile(r"(^INSERT|\*;\*|)")
getValidator = re.compile(r"(^SELECT|\*;\*|)")


def main():
    """Main."""
    config = ConfigParser()

    # parse existing file
    print(os.path.dirname(os.path.realpath(__file__))+'/cloud.ini')
    print(config.read(os.path.dirname(os.path.realpath(__file__))+'/cloud.ini'))

    # read values from a section
    host = '0.0.0.0'
    port = int(config.get('GateKeeper', 'port'))
    destination = config.get('GateKeeper', 'destination')

    s = socket.socket()
    s.bind((host, port))
    s.listen(1)  # Listen to one connection

    conn, addr = s.accept()
    print('connection from: ' + str(addr))

    trustedSocket = socket.socket()
    destIp = config.get(destination, 'ip')
    destPort = int(config.get(destination, 'port'))
    trustedSocket.connect((destIp, destPort))

    while True:
        data = conn.recv(409600)  # Max bytes
        print('Data: ' + str(data))
        if not data:
            break
        print('from connected user: ' + str(data))

        if not validate(str(data)):
            break

        strData = str(data)

        print("Connected to the trusted host!")
        trustedSocket.send(data)

    trustedSocket.close()

def validate(data):
    if "INSERT" in data:
        return bool(postValidator.match(data))
    if "SELECT" in data:
        return bool(postValidator.match(data))
    return False

if __name__ == '__main__':
    main()

