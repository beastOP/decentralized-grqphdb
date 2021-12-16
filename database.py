from graph import Database
import threading
import socket
import getopt
import sys
import json
from random import randint

opts, args = getopt.getopt(sys.argv[1:], "p:i:")
PORT = int(opts[0][1]) if len(opts) > 0  else 50001
ID = opts[1][1] if len(opts) > 1  else "Au9X"
peer_port = PORT+1 if PORT-50000 ==1 else PORT-1
peer = ('127.0.0.1', peer_port)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', PORT))
print("Connecting peers!")
sock.sendto(b'ping', peer)

while True:
    data, address = sock.recvfrom(128)
    sock.sendto(b'ping', address)
    if data.decode() == 'ping':
        break

print("Online!")
DATA = Database(ID)
PREV = ""

def handle_data(data, address):
    data = data.split("-")
    if data[0] == "ADD":
        idx = DATA.add_node(json.loads(data[1]), *list([2]))
        sock.sendto(idx.encode(), address)
    elif data[0] == "MATCH":
        dta = DATA.match()
        sock.sendto((json.dumps(dta)).encode(), address)
    elif data[0] == "RADD":
        print(data[1]+"-"+data[2], data[3]+"-"+data[4])
        idx = DATA.add_relation(data[1]+data[2], data[3]+data[4], {}, "users")
        if type(idx) != str:
            str(idx)
        sock.sendto(idx.encode(), address)

try:
    while True:
        data, address = sock.recvfrom(10000)
        if data.decode() == 'ping':
            continue
        elif data.decode() == 'dead':
            print("no peers alive....so, shuting down")
            print(DATA.match())
            sock.close()
            sys.exit(1)
        t = threading.Thread(target=handle_data, args=[data.decode(), address])
        t.start()
except KeyboardInterrupt:
    sock.sendto(b'dead', peer)
    sock.close()
    print(DATA.match())
    sys.exit(1)
