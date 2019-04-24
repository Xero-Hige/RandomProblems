import socket
from socket_handler import Socket
  
def main():
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
		skt.connect(("127.0.0.1",9090))
		skt = Socket(skt)

		input_data = input("--:")

		while input_data:
			skt.write_to_socket(input_data)
			print("Response",skt.read_from_socket())

			input_data = input("--:")

		skt.write_to_socket("END")

if __name__ == '__main__':
	main()