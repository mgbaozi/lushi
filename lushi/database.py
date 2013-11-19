from pymongo import MongoClient
import json

class DataBase(object):
	def __init__(self):
		self._db_clients = {}
		db_configs = None
		with open("config/database.json") as fp:
			db_configs = json.load(fp)
		for name, config in db_configs.items():
			connection = MongoClient(config["address"], config["port"])
			db = connection.__getattr__(config["database"])
			collection = db.__getattr__(config["collection"])
			self._db_clients[name] = collection
	def __getattr__(self, attr):
		return self._db_clients.get(attr)

