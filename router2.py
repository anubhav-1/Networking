import socket
import time
import _thread
import difflib

s= socket.socket()
s_host=socket.gethostbyname(socket.gethostname())
s_port= 12372
s.bind((s_host, s_port))



pack=[]
s.listen(10)

while True:
    c, addr = s.accept()
    print("Got connection from: " + str(addr))
    content= c.recv(1024).decode()
    x=eval(content)['packetNumber']
    #print(len(content))
    y=eval(content)['numberOfPackets']
    #print(y)
    pack.append(content)
    msg = 'success'
    c.send(msg.encode())

    if abs(int(x)-int(y)) == 1:
        s.close()
        break


for item in pack:
    k = socket.socket()
    k_host = socket.gethostbyname(socket.gethostname())
    k_port = 12373
    k.connect((k_host, k_port))
    k.send(str(item).encode())
    print("Sent: "+str(item))
    print(k.recv(1024).decode())
    k.close()


k.close()
