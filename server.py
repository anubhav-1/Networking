import socket
import time
import _thread
import difflib


certi='abc'
private_key=None
public_key=None

def keys():
    global private_key
    global public_key
    global n
    global e
    p1 = 53
    p2 = 59
    n = p1 * p2
    phi = (p1 - 1) * (p2 - 1)
    e=3
    private_key = int(((2 * phi) + 1) / e)
    public_key = (n, e)

    print("Private: "+str(private_key)+" Public: "+str(public_key))
    o=socket.socket()
    host=socket.gethostbyname(socket.gethostname())
    port=12388
    o.connect((host,port))
    o.send(str(['192.168.10.127',public_key]).encode())
    print("Keys sent")
    o.recv(1024)
    o.close()



def certi_check(immediate_senderIP):
    global certi
    m='a'

    #certificate Check
    k=socket.socket()
    k_host = socket.gethostbyname(socket.gethostname())
    k_port = 12350
    k.connect((k_host, k_port))

    try:
        k.send(immediate_senderIP.encode())

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
    s_port= 12376
    s.bind((s_host, s_port))
    #filename = "received.py"

    s.listen(10)

    while True:
        c, addr = s.accept()

        pack = eval(c.recv(1024).decode())
        info=str(pack['payload'])
        info_arry=eval(info)
        temp =str(pack['certificate'])
        filename=str(pack['nameOfInfo'])


        patharray=pack['ipPath']
        immediate_senderIP=str(patharray[-1])
        print("Got connection from: " + str(immediate_senderIP))
        print(info_arry)
        print(temp)
        print(filename)
        print("Public Key is: "+ str(public_key))


        again=''
        for i in info_arry:
            i=int((int(i)**private_key)%n)
            again=again+chr(int(i))
        if certi=='abc':
            try:
                certi_check(immediate_senderIP)
                time.sleep(1)

            except:
                print("Cannot Verify Certificate.")


        print(temp+" "+str(type(temp)))
        if certi == temp:
            file = open(filename, "a+")
            data= info
            file.write(again)
            print("written")
            file.close()
            msg = 'success'
            c.send(msg.encode())







try:
    _thread.start_new_thread(receive_data, ())
    _thread.start_new_thread(keys, ())
    #_thread.start_new_thread(certi_check, ())

except:
    print("Cannot Create Thread....")

while 1:
    pass

