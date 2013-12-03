from proto_global import global_pool, global_factory

def get_message(type_name):
	descriptor = global_pool.FindMessageTypeByName(type_name)
	if descriptor:
		prototype = global_factory.GetPrototype(descriptor)
		message = prototype() if prototype else None
	return message

def get_name(message):
	return message.DESCRIPTOR.full_name

