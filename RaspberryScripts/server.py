import socket

host, port = '192.168.7.153', 2121 # enter ipv4 address of pc which is in the same network
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	s.bind((host, port))
except:
	print("Failed to bind")

s.listen(5)
print("Waiting for data")

(conn, addr) = s.accept()
print("Connected")

while True:
	#data = conn.recv(1024)
	#print("Received:", data.decode('utf-8'))
	reply = input("Vector: ")
	conn.send(reply.encode('utf-8'))

conn.close()
