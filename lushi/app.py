from packet import register, get_function
import codec
from receiver import TcpReceiver, set_receiver, run_all

class ProtoRouter(object):
	def route(self, msg_type, **options):
		def decorator(f):
			register(msg_type, f, **options)
			return f
		return decorator

	def run(self, port=[], debug=None):
		self.debug = debug
		set_receiver(self._get, port)
		run_all()

	def _get(self, data):
		message = codec.parse(data)
		if message:
			fn = get_function(message)
			if fn:
				return lambda x: fn(x, message)
			else:
				return None	
		else:
			return None

	def make_packet(self, message):
		return codec.package(message) 
