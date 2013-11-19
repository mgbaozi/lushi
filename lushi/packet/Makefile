pb = login_pb2.py

$(pb): %_pb2.py: %.proto
	protoc --python_out=. $<

.PHONY: clean
clean:
	rm -f *_pb2.py
	rm -f *.pyc
