from uuid import getnode as get_mac
import math
import socket
import random
import time
from tkinter.filedialog import askopenfilename
from tkinter import *


class Packet(object):
    """docstring for Packet"""

    def __init__(self, senderIP, senderMAC, receiverIP, nameOfInfo, packetNumber, numberOfPackets, payload,
                 certificate,ipPath):
        self.senderIP = senderIP
        self.senderMAC = senderMAC
        self.receiverIP = receiverIP
        self.nameOfInfo = nameOfInfo
        self.packetNumber = packetNumber
        self.numberOfPackets = numberOfPackets
        self.payload = payload
        self.certificate = certificate
        self.ipPath = ipPath


def get_keys(senderIP):
    global dest_public_key
    o=socket.socket()
    host=socket.gethostbyname(socket.gethostname())
    port=12389
    o.connect((host,port))
    o.send(str(senderIP).encode())
    dest_public_key= eval(o.recv(1024).decode('ascii'))


def num(message):
    return math.ceil(len(message)/10)


def getCerti(senderIP):
    s=socket.socket()
    # ip of Certificate Server
    host=socket.gethostbyname(socket.gethostname())
    port=12345
    s.connect((host,port))
    s.send(senderIP.encode())
    t=str(s.recv(1024).decode('ascii'))
    print("Fetched Certificate: "+str(t))
    s.close()
    return t


def setValues():
    global senderIP, senderMAC, receiverIP, nameOfInfo, payload, numberOfPackets, certificate, ipPath
    ipPath=[]
    senderIP = '192.168.10.120'
    senderMAC = get_mac()
    receiverIP = input("Enter the receiver IP: ")
    # Calculate public Key
    p1 = 53
    p2 = 59
    n = p1 * p2
    phi = (p1 - 1) * (p2 - 1)
    e=3
    private_key = int(((2 * phi) + 1) / e)
    public_key = (n, e)
    get_keys(receiverIP)

    n1=dest_public_key[0]
    e1 = dest_public_key[1]

    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    payload_file = askopenfilename()  # show an "Open" dialog box and return the path to the selected file

    payload = open(payload_file, "r+").read()
    msg=''
    for alpha in payload:
        temp = ord(alpha)
        print("temp old: "+str(temp))
        temp=(temp**e1)%n1
        msg=msg+str(temp)+str(' ')
        print(alpha+' -> '+ str(temp)+' -> '+str(msg))

    msg=msg.split(' ')
    msg.pop()
    payload=msg

    numberOfPackets = num(payload)

    nameOfInfo=payload_file.split('/')[-1]
    certificate = getCerti(senderIP)
    ipPath.append(senderIP)


def sendData():


    pack = []
    counter = 0
    filename = "records.txt"
    for i in range(numberOfPackets):
        pack.append(
            Packet(senderIP, senderMAC, receiverIP, nameOfInfo, i, numberOfPackets, payload[counter:counter + 10],
                   certificate,ipPath))
        counter = counter + 10


    zy = input()
    com_packet = {}
    print("Transmitting Data...")

    c = 1
    file = open(filename, "a+")
    file.write("Record\n")
    for item in pack:
        k = socket.socket()

        # ip of the router1
        host = socket.gethostbyname(socket.gethostname())
        port = 12371

        k.connect((host, port))

        file.write(str(item.senderIP) + "\n")
        com_packet["senderIP"] = str(item.senderIP)
        file.write(str(item.senderMAC) + "\n")
        com_packet["senderMAC"] = str(item.senderMAC)
        file.write(str(item.receiverIP) + "\n")
        com_packet["receiverIP"] = str(item.receiverIP)
        file.write(str(item.nameOfInfo) + "\n")
        com_packet["nameOfInfo"] = str(item.nameOfInfo)
        file.write(str(item.packetNumber) + "\n")

        com_packet["packetNumber"] = str(item.packetNumber)
        file.write(str(item.numberOfPackets) + "\n")
        com_packet["numberOfPackets"] = str(item.numberOfPackets)
        file.write(str(item.payload) + "\n")
        com_packet["payload"] = str(item.payload)
        file.write(str(item.certificate) + "\n")
        com_packet["certificate"] = str(item.certificate)

        file.write(str(item.ipPath) + "\n")
        com_packet["ipPath"] = item.ipPath



        print(len(str(com_packet)))
        print(com_packet)
        k.send(str(com_packet).encode())
        print("Packet " + str(c) + " of " + str(len(pack)) + " Sent")
        c = c + 1
        # if k.recv(1024) == True:
        #     print("Acknowleggement Recieved...")

        k.close()

    file.close()



setValues()
sendData()

