import socket
import pickle as serializer

class Socket():

	def __init__(self,socket):
		self.skt = socket
		
	def _read_from_socket(self,lenght=5):
		data = self.skt.recv(lenght)
		received = data

		while len(data) < lenght and received:
			received += self.skt.recv(lenght-len(received))
			data += received

		return serializer.loads(received)

	def read_from_socket(self):
		lenght = self._read_from_socket()
		data = self._read_from_socket(lenght)

		return data

	def write_to_socket(self,data):
		data = serializer.dumps(data)
		lenght = len(data)

		self.skt.sendall(serializer.dumps(lenght))
		self.skt.sendall(data)