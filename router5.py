import socket
import time
import _thread
import difflib

def cross_communication_sender():
    pass

def cross_communication_reciever():
    pass


def rest():
    # Get Certi
    def get_certi(myIP):
        g = socket.socket()
        # ip of Certificate Server
        host = socket.gethostbyname(socket.gethostname())
        port = 12345
        g.connect((host, port))
        g.send(myIp.encode())
        t = str(g.recv(1024).decode('ascii'))
        print("Fetched Certificate: " + str(t))
        g.close()
        return t




    certi='abc'

    def certi_check(senderIP):

        m = 'a'

        # certificate Check
        z = socket.socket()
        z_host = socket.gethostbyname(socket.gethostname())
        z_port = 12350
        z.connect((z_host, z_port))

        try:
            z.send(senderIP.encode())

        except NameError:
            print("Waiting....")

        else:
            m = 'abc'
            certi = str(z.recv(1024).decode('ascii'))
            certi = certi.rstrip("\n")
            print("Issued Certificate was: " + certi + " " + str(type(certi)))
            z.close()
            return certi



    myIp='192.168.10.125'
    my_certificate=get_certi(myIp)


    s= socket.socket()
    s_host=socket.gethostbyname(socket.gethostname())
    s_port= 12375
    s.bind((s_host, s_port))




    pack=[]
    s.listen(10)

    while True:
        c, addr = s.accept()

        content= c.recv(1024).decode()
        x=eval(content)['packetNumber']
        patharray = eval(content)['ipPath']
        senderIP = str(patharray[-1])
        print("Got connection from: " + str(senderIP))
        #print(len(content))
        y=eval(content)['numberOfPackets']
        certi_pack = eval(content)['certificate']

        if certi == 'abc':
            try:
                checked_certificate=certi_check(senderIP)
                time.sleep(1)
                certi='checked'

            except:
                print("Cannot Verify Certificate.")

        #print(y)
        if checked_certificate == certi_pack:
            out=eval(content)
            out['certificate']=str(my_certificate)
            out['ipPath'].append(myIp)
            pack.append(str(out))
            msg = 'success'
            c.send(msg.encode())

        if abs(int(x)-int(y)) == 1:
            s.close()
            break


    for item in pack:
        k = socket.socket()
        k_host = socket.gethostbyname(socket.gethostname())
        k_port = 12376
        k.connect((k_host, k_port))
        k.send(str(item).encode())
        print("Sent: "+str(item))
        print(k.recv(1024).decode())
        k.close()



try:
    _thread.start_new_thread(rest, ())
    _thread.start_new_thread(cross_communication_sender, ())
    _thread.start_new_thread(cross_communication_reciever, ())

except:
    print("Cannot Create Thread....")

while 1:
    pass
