import socket
import random
import string
import _thread

def reg():
    s = socket.socket()
    host = socket.gethostbyname(socket.gethostname())
    port = 12388
    s.bind((host, port))

    s.listen(10)
    while True:
        c, addr = s.accept()
        combine= eval(c.recv(1024).decode('ascii'))
        senderIP=combine[0]
        public_key=str(combine[1])
        print("Got ISSUE request from: " + str(senderIP))


        with open("key_records.txt", "a+") as file:
            a = [senderIP, public_key]
            file.write("; ".join(a))
            file.write("\n")
            file.close()
            msg = str('success')
            c.send(msg.encode())
            c.close()


def give():
    k = socket.socket()
    host = socket.gethostbyname(socket.gethostname())
    port = 12389
    k.bind((host, port))

    k.listen(10)
    while True:
        c, addr = k.accept()
        ip = c.recv(1024).decode('ascii')
        print("ip: " + str(ip))

        filename = "key_records.txt"
        file = open(filename, "r")
        result = "a"
        for lines in file:
            result = lines.split("; ")


            if str(result[0]) == str(ip):
                c.send(result[1].encode())

        print("Public Key sent is: "+ str(result[1]))
        c.close()

try:
    _thread.start_new_thread(reg, ())
    _thread.start_new_thread(give, ())

except:
    print("Cannot Create Thread....")

while 1:
    pass



