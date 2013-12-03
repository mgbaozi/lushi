from router import ProtoRouter

from database import DataBase

app = ProtoRouter()
db = DataBase()

import memcache
cache = memcache.Client(['127.0.0.1:11211'])

@app.route(connection.Connect)
def on_connect(conn, message):
	token = messae.token
	account = cache.get(token)
	if not account:
		conn.send("out of time")
		return
	conn.send("successful")
