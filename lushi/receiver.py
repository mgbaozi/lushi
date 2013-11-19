from twisted.internet.protocol import Protocol, Factory
from tornado.platform.twisted import TwistedIOLoop
from twisted.internet import reactor

TwistedIOLoop().install()

from tornado.websocket import WebSocketHandler
import tornado.web

from twisted.python import log
import sys
log.startLogging(sys.stdout)

import struct

k_header_len = 4
k_min_msg_len = 2
class TcpReceiver(Protocol):
	def __init__(self, function_getter):
		log.msg("connection")
		self._buffer = ''
		self._function_getter = function_getter

	def dataReceived(self, data):
		self._buffer += data
		while len(self._buffer) >= k_header_len + k_min_msg_len:
			length = struct.unpack('>i', buffer(self._buffer, 0, k_header_len))[0]
			if len(self._buffer) >= length + k_header_len:
				message = buffer(self._buffer, k_header_len, length)
				function = self._function_getter(message)
				if function:
					function(self)
				self._buffer = self._buffer[k_header_len+length:]
			else:
				break

	def send(self, message):
		data = struct.pack('>i', len(message)) + message
		self.transport.write(data)

class WebSocketReceiver(WebSocketHandler):
	_function_getter = None
	def open(self):
		log.msg("WebSocket Connection")

	def on_message(self, message):
		function = self._function_getter(message)
		if function:
			function(self)

	def send(self, message):
		self.write_message(message)

class ReceiverFactory(Factory):
	def __init__(self, protocol, function_getter):
		self._protocol = protocol
		self._function_getter = function_getter

	def buildProtocol(self, addr):
		return self._protocol(self._function_getter)

def set_receiver(function_getter, port):
	reactor.listenTCP(port[0], ReceiverFactory(TcpReceiver, function_getter))
	WebSocketHandler._function_getter = function_getter
	application = tornado.web.Application([(u"/", WebSocketReceiver),])
	application.listen(port[1])

def run_all():
	reactor.run()
