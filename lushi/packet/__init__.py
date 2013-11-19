from google.protobuf import descriptor_pb2
import login_pb2 as login

from proto_global import global_pool

from message import get_message, get_name, register, get_function

_modules = [login]

for module in _modules:
	file_string = module.DESCRIPTOR.serialized_pb
	fd = descriptor_pb2.FileDescriptorProto.FromString(file_string)
	global_pool.Add(fd)
