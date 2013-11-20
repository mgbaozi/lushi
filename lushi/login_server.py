from router import ProtoRouter
from packet import login
import json

import hashlib
import uuid

from database import DataBase
app = ProtoRouter()
db = DataBase()
collection = db.users

import memcache
cache = memcache.Client(['127.0.0.1:11211'])

server_list_rep = login.ServerList()
with open("config/server_list.json") as fp:
	server_list = json.load(fp).get("servers")
	for server in server_list:
		server_rep = server_list_rep.servers.add()
		server_rep.name = server["name"]
		server_rep.address = server["address"]
		server_rep.port = server["port"]
		server_rep.load = login.Server.LOW

@app.route(login.Request)
def on_request(conn, message):
	account = message.account
	passwd = message.passwd
	passwd = hashlib.md5(passwd).hexdigest()
	user = collection.find_one({"account":account})
	rep = login.Response()
	rep.err = login.Response.SUCCESS
	rep.token = ""
	if not user:
		rep.err = login.Response.ACCOUNT_NOT_EXIST
	else:
		if not user["passwd"] == passwd:
			rep.err = login.Response.WRONG_PASSWD
		else:
			token = uuid.uuid1().get_hex()
			rep.token = token
			cache.set(token, account, 300)
	response = app.make_packet(rep)
	conn.send(response)

@app.route(login.Empty)
def on_empty(conn, message):
	response = app.make_packet(server_list_rep)
	conn.send(response)

if __name__ == "__main__":
	app.run([23333, 23334])
