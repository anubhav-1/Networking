import socket

s=socket.socket()
host=socket.gethostbyname(socket.gethostname())
port= 12350
s.connect((host,port))
ip='127.0.0.1'
s.send(ip.encode())
certi=s.recv(1024).decode('ascii')
print(certi)
s.close()
import socket

s=socket.socket()
host=socket.gethostbyname(socket.gethostname())
port= 12350
s.connect((host,port))
ip='127.0.0.1'
s.send(ip.encode())
certi=s.recv(1024).decode('ascii')
print(certi)
s.close()
