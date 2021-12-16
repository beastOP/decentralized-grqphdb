import socket
import json
import sys
from random import randint
from flask import Flask, request

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 55555))

databases = [('127.0.0.1', 50001),('127.0.0.1', 50002)]

app = Flask(__name__)

@app.route("/")
def index():
    return 'Hello World'

@app.route("/add", methods=["POST"])
def add():
    query = request.data
    query = json.loads(query)
    data, lable = query["data"], query["lable"]
    rnd = randint(0, 10)
    sock.sendto(f'ADD-{json.dumps(data)}-{lable}'.encode(), databases[rnd%2])
    idx = sock.recv(1024)
    return json.dumps({ "success": 200, "id": idx.decode()}), 200

@app.route("/update", methods=["POST"])
def update():
    query = request.data
    query = json.loads(query)
    _id, data, lable = query["id"], query["data"], query["lable"]
    rnd = randint(0, 10)
    print(_id, data, lable)
    sock.sendto(f'UPDATE-{_id}-{data}-{lable}'.encode(), databases[rnd%2])
    idx = sock.recv(1024)
    return json.dumps({ "success": 200, "id": idx.decode()}), 200

@app.route("/delete/<_id>")
def delete(_id):
    sock.sendto(f'DELETE-{_id}'.encode(), databases[rnd%2])
    result = sock.recv(1024)
    return json.dumps({ "success": 200 }), 200

@app.route("/add_relation", methods=["POST"])
def add_relation():
    query = request.data
    query = json.loads(query)
    _from, to, data, lable = query["from"], query["to"], query["data"], query["lable"]
    print(_from, to)
    rnd = randint(0, 10)
    sock.sendto(f'RADD-{_from}-{to}-{data}-{lable}'.encode(), databases[rnd%2])
    return json.dumps({ "success": 200 }), 200

@app.route('/match', methods=["POST", "GET"])
def match():
    query = request.data
    rnd = randint(0, 10)
    if query != b'':
        matches = json.loads(query)["query"]
        sock.sendto(f'MATCH-{matches}'.encode(), databases[0])
        sock.sendto(f'MATCH-{matches}'.encode(), databases[1])
    else:
        sock.sendto('MATCH- '.encode(), databases[0])
        sock.sendto('MATCH- '.encode(), databases[1])
    data1 = sock.recv(100000)
    data2 = sock.recv(100000)
    data = json.loads(data1.decode()) +json.loads(data2.decode())
    return json.dumps({ "data": data }), 200


if __name__ == '__main__':
    try:
        app.run(threaded=True)
    except KeyboardInterrupt:
        sock.close()
        sys.exit()
