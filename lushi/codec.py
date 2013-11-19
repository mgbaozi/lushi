from packet import get_message, get_name
import struct
k_header_len = 4
def parse(data):
	name_len = struct.unpack('>i', buffer(data, 0, k_header_len))[0]
	type_name = data[k_header_len : k_header_len + name_len - 1]
	message = get_message(type_name)
	if message:
		proto_data = buffer(data, k_header_len + name_len, len(data) - name_len - k_header_len)
		try:
			message.ParseFromString(proto_data)
		except:
			message = None
	else:
		pass
	return message

def package(message):
	type_name = get_name(message)
	name_len = len(type_name) + 1
	byte_size = message.ByteSize()
	data = struct.pack('>i', name_len) + type_name + struct.pack('>c', '\0') + message.SerializeToString()
	return data	
