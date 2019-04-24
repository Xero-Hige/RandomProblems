import csv
import threading
import socket
import signal
from socket_handler import Socket

def prob_between(node_a,node_b,graph,min_prob=0):
	queue = [(node_a,1)]
	visited = set()

	while queue:
		print(node_a,node_b,queue)
		node,prob = queue.pop(0)

		if node == node_b:
			return prob if prob >= min_prob else 0

		for _node,_node_prob in graph[node]:
			if prob < min_prob or _node in visited:
				continue

			print(prob,min_prob)
			queue.append( (_node,prob*_node_prob) )

		visited.add(node)

	return 0

def handle_connection(graph,skt):
	request = skt.read_from_socket()

	print("Request: ",request)

	while request and request != "END":
		node_a,node_b,prob_exp = request.split(",")
		prob = 10**float(prob_exp)
		calculated_prob = prob_between(node_a,node_b,graph,prob)
		
		skt.write_to_socket('Yes' if calculated_prob else 'No')
		request = skt.read_from_socket()



MAX_THREADS = 2

class Server():

	def __init__(self,config_file):
		self.graph = {} 
		self.semaphore = threading.BoundedSemaphore(value=MAX_THREADS)
		self.thread_list_lock = threading.BoundedSemaphore(value=1)
		self.ended_threads = []
		self.threads = [None for _ in range(MAX_THREADS) ]
		self._thread_position = 0

		with open(config_file) as config:
			for node_a,node_b,prob in csv.reader(config):
				self.graph[node_a] = self.graph.get(node_a,[])
				self.graph[node_b] = self.graph.get(node_b,[])
				prob = int(prob)/100
				self.graph[node_a].append((node_b,prob))
				self.graph[node_b].append((node_a,prob))

	def accept_conections(self):
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as skt:
			skt.bind(("127.0.0.1",9090))
			skt.listen(50)

			def handler(signum, frame):
				skt.shutdown(socket.SHUT_RDWR)
				skt.close()

			signal.signal(signal.SIGINT,handler)

			try:
				conn,addr = skt.accept()
			except OSError as e:
				conn = None


			while conn:
				self.handle_connection(conn)
				try:
					conn,addr = skt.accept()
				except OSError as e:
					conn = None

		for thread in self.threads:
			if thread:
				thread.join()

	def handle_connection(self,conection):

		self.semaphore.acquire()

		with self.thread_list_lock:
			while self.ended_threads:
				thread = self.ended_threads.pop()
				self.threads[thread].join()
				self.threads[thread] = None

		while self.threads[self._thread_position]:
			self._thread_position += 1
			self._thread_position %= MAX_THREADS

		def _handler():
			try:
				handle_connection(self.graph,Socket(conection))
			finally:
				conection.close()
				with self.thread_list_lock:
					self.ended_threads.append(self._thread_position)
				
				self.semaphore.release()

		self.threads[self._thread_position] = threading.Thread(target=_handler)
		self.threads[self._thread_position].start()
		
if __name__ == '__main__':
	server = Server("config.txt")
	server.accept_conections()