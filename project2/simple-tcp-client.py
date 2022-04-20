## Imports 
from multiprocessing import Value
from threading import Timer
from util import*
import multiprocessing
import random
import socket
import time
import sys


def send(sock,message,IP,Port,type):
    sock.sendto(message, (IP, Port))
    printSending(int(message[:16], 2),type)


#Helper Method for seqNum
def rand_int():
	return random.randint(0,(2 ** 5)-1)


class Client:
    def __init__(self,sock,IP,Port):
        self.closed = True
        self.syn = False
        self.handshake()
        self.sock = sock
        self.IP = IP
        self.Port = Port
    def handshake(self):
        if self.closed:
            seqNum = rand_int()
            synHeader = Header(seqNum,0,1,0,1,0)
            send(self.sock,synHeader.bytes(),self.IP,self.Port,"SYNACK")
            self.closed = False
        else:
            pass

    def terminate(self):
        pass
    
    def send_tcp(self,message):
        pass

    def checkAck(self,lastAck):
        go = True
        while go:
            data , addr = self.sock.recvfrom(1024)
            header = decodeHeader(data)
            if header.ackNum > lastAck:
                lastAck.value = header.ackNum
    def recvAck(self):
        lastAck = Value('i', self.lastAck)
        multi = multiprocessing.Process(target = self.checkAck,args = (lastAck))
        multi.start()
        multi.join(1)
        if multi.is_alive():
            multi.terminate()
            multi.join()
        self.lastAck = lastAck.value


#Main Method 
def main(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    client = Client(sock,ip,port)
    client.send_tcp('THIS IS A TEST THAT WILL BE SENT IN MULTIPLE PIECES LOLOLOLOLOLOLOL HEHH')
    client.terminate()


if __name__ == "__main__":
    if len(sys.argv) != 3: 
        sys.exit("Usage: python simple-tcp-client.py SERVER-HOST-OR-IP PORT-NUMBER") 
    receiver_ip = sys.argv[1] 
    receiver_port = int(sys.argv[2])
    main(receiver_ip,receiver_port)
