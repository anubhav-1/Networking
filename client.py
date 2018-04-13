from uuid import getnode as get_mac
import math
import socket
import time
from tkinter.filedialog import askopenfilename
from tkinter import *


class Packet(object):
    """docstring for Packet"""

    def __init__(self, senderIP, senderMAC, receiverIP, nameOfInfo, packetNumber, numberOfPackets, payload,
                 certificate):
        self.senderIP = senderIP
        self.senderMAC = senderMAC
        self.receiverIP = receiverIP
        self.nameOfInfo = nameOfInfo
        self.packetNumber = packetNumber
        self.numberOfPackets = numberOfPackets
        self.payload = payload
        self.certificate = certificate

def num(message):
    return math.ceil(len(message)/10)


def getCerti():
    s=socket.socket()
    # ip of Certificate Server
    host=socket.gethostbyname(socket.gethostname())
    port=12345
    s.connect((host,port))
    t=str(s.recv(1024).decode('ascii'))
    print("Fetched Certificate: "+str(t))
    s.close()
    return t


def setValues():
    global senderIP, senderMAC, receiverIP, nameOfInfo, payload, numberOfPackets, certificate
    senderIP = socket.gethostbyname(socket.gethostname())
    senderMAC = get_mac()
    receiverIP = input("Enter the receiver IP: ")

    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    payload_file = askopenfilename()  # show an "Open" dialog box and return the path to the selected file

    payload = open(payload_file, "r+").read()

    numberOfPackets = num(payload)

    nameOfInfo=payload_file.split('/')[-1]
    certificate = getCerti()


def sendData():
    pack = []
    counter = 0
    filename = "records.txt"
    for i in range(numberOfPackets):
        pack.append(
            Packet(senderIP, senderMAC, receiverIP, nameOfInfo, i, numberOfPackets, payload[counter:counter + 10],
                   certificate))
        counter = counter + 10


    zy = input()
    com_packet = {}
    print("Transmitting Data...")

    c = 1
    file = open(filename, "a")
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

