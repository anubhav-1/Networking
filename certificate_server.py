import socket
import random
import string
import _thread

def issue():
    s = socket.socket()
    host = socket.gethostbyname(socket.gethostname())
    port = 12345
    s.bind((host, port))

    s.listen(10)
    while True:
        c, addr = s.accept()
        print("Got ISSUE request from: " + str(addr))



        obtain = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        print("Issued Certificate ID: " + str(obtain) + " to: " + str(addr[0]))

        with open("Certificate_records.txt", "a") as file:
            a = [str(addr[0]), obtain]
            file.write(", ".join(a))
            file.write("\n")
            file.close()
            msg = str(obtain)
            c.send(msg.encode())
            c.close()


def check():
    k = socket.socket()
    host = socket.gethostbyname(socket.gethostname())
    port = 12350
    k.bind((host, port))

    k.listen(10)
    while True:
        c, addr = k.accept()
        ip = c.recv(1024).decode('ascii')
        print("ip: " + str(ip))
        print("Got CHECK request from: " + str(addr))
        filename = "Certificate_records.txt"
        file = open(filename, "r")
        result = "a"
        for lines in file:
            result = lines.split(", ")


            if str(result[0]) == str(ip):
                c.send(result[1].encode())

        print("Cerificate sent is: "+ str(result[1]))
        c.close()

try:
    _thread.start_new_thread(issue, ())
    _thread.start_new_thread(check, ())

except:
    print("Cannot Create Thread....")

while 1:
    pass



