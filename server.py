import socket
import time
import _thread
import difflib


certi='abc'

def certi_check():
    global certi
    m='a'

    #certificate Check
    k=socket.socket()
    k_host = socket.gethostbyname(socket.gethostname())
    k_port = 12350
    k.connect((k_host, k_port))

    try:
        k.send(addr[0].encode())

    except NameError:
        print("Waiting....")

    else:
        m='abc'
        certi = str(k.recv(1024).decode('ascii'))
        certi=certi.rstrip("\n")
        print("Issued Certificate is: "+certi+" "+str(type(certi)))





def receive_data():
    global c, addr
    global certi
    temp='mno'
    data='temp'
    #receiving info
    s= socket.socket()
    s_host=socket.gethostbyname(socket.gethostname())
    s_port= 12373
    s.bind((s_host, s_port))
    #filename = "received.py"

    s.listen(10)

    while True:
        c, addr = s.accept()
        print("Got connection from: " + str(addr))
        pack = eval(c.recv(1024).decode())
        info=str(pack['payload'])
        temp =str(pack['certificate'])
        filename=str(pack['nameOfInfo'])
        print(info)
        print(temp)
        print(filename)
        if certi=='abc':
            try:
                _thread.start_new_thread(certi_check, ())
                time.sleep(1)

            except:
                print("Cannot Verify Certificate.")


        print(temp+" "+str(type(temp)))
        if certi == temp:
            file = open(filename, "a+")
            data= info
            file.write(data)
            print("written")
            file.close()
            msg = 'success'
            c.send(msg.encode())







try:
    _thread.start_new_thread(receive_data, ())
    #_thread.start_new_thread(certi_check, ())

except:
    print("Cannot Create Thread....")

while 1:
    pass

