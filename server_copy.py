import socket


def fetch_certi():
    # certificate Check
    k = socket.socket()
    k_host = socket.gethostbyname(socket.gethostname())
    k_port = 12350
    k.connect((k_host, k_port))
    k.send(addr[0].encode())

    certi = k.recv(1024).decode('ascii')
    k.close()
    return certi





global c, addr
#receiving info
s= socket.socket()
s_host=socket.gethostbyname(socket.gethostname())
s_port= 12348
s.bind((s_host, s_port))

counter=0
filename = "received.py"
s.listen(10)
while True:
    counter=counter+1
    c, addr = s.accept()
    print("Got connection from: " + str(addr))

    if counter==1:
        certi= fetch_certi()


        print("issued Certificate is: "+str(certi))

    print("certi in packets: "+ str(eval(c.recv(1024))['certificate']))

    print(eval(c.recv(1024)).decode('ascii'))
    #if str(certi) == eval(c.recv(1024))['certificate']:
    file = open(filename, "a+")
    file.write(eval(c.recv(1024))['payload'])
    file.close()
    msg = 'success'
    c.send(msg.encode())
    c.close()



# try:
#     _thread.start_new_thread(receive_data, ())
#     _thread.start_new_thread(certi_check, ())

# except:
#     print("Cannot Create Thread....")

# while 1:
#     pass

