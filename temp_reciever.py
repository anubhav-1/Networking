import socket
s= socket.socket()
s_host=socket.gethostbyname(socket.gethostname())
s_port= 12372
s.bind((s_host, s_port))
s.listen(10)
c,addr=s.accept()
print(c.recv(1024))
c.close()