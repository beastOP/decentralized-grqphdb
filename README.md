# Decentralised graph database management system
## To get started
clone the repo, and run the command below.
```bash
python3 database.py
```
Now, create a new terminal instance and run the following command.
```bash
python3 database.py -p 50002 -i Bmz9
```
> ```-p``` is for specifing port (but, please stick with 50002 for this to work) and ```-i``` is for specifing a instance id for this database instance.
Then run,
```bash
pip install flask
python3 server.py
```
## To add data
Run the following request,
```bash
curl -H 'Content-Type: application/json' http://127.0.0.1:5000/add -XPOST -d '{"data": {"username": "beastOP"}, "lable":["git_users"]}'
```
and to get the data run
```bash
curl http://127.0.0.1:5000/match
```
