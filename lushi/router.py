from packet import get_name
import codec
from receiver import TcpReceiver, set_receiver, run_all

class ProtoRouter(object):
	def __init__(self):
		self._functions = {}

	def _register(self, msg_type, function):
		self._functions[get_name(msg_type)] = function

	def _get_function(self, message):
		return self._functions.get(get_name(message))

	"""
	app = ProtoRouter()
	# and use it like this
	-----------------------
	@app.route(module.Query)
	def onQuery(conn, message):
		answer = mudule.Answer()
		conn.send(app.make_packet(answer))
	-----------------------
	"""
	def route(self, msg_type, **options):
		def decorator(f):
			self._register(msg_type, f, **options)
			return f
		return decorator

	"""
	app.run([portToTCP, portToWebSocket])
	"""
	def run(self, port=[], debug=None):
		self.debug = debug
		set_receiver(self._get, port)
		run_all()

	def _get(self, data):
		message = codec.parse(data)
		if message:
			fn = self._get_function(message)
			if fn:
				return lambda x: fn(x, message)
			else:
				return None	
		else:
			return None

	def make_packet(self, message):
		return codec.package(message) 
