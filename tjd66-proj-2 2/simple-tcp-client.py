## Imports 
from multiprocessing import Value
from threading import Timer
import util
from util import*
import multiprocessing
import random
import socket
import time
import sys

#Main Method 
def main(ip,port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    serveraddress = (str(ip), port)
    # TRY TO CONNECT 
    seqNum = rand_int()
    synHeader = Header(seqNum, 0, 1, 0 , 1, 0)
    sent = sock.sendto(synHeader.bytes(),serveraddress)
    starttime = time.time()
    if sent: 
        printSending(seqNum,"SYN")
    ## CONNECTION TO SERVER 
    go = True
    listening = True
    sendACK = False
    lastheader = synHeader
    timego = True

    while go: 
        if listening: 
            data,addr = sock.recvfrom(1024)
            if data:
                header = util.decodeHeader(data)
                #RETRANSMISSION
                if header.ackNum != lastheader.seqNum + 1 or ((starttime - time.time()) > 0.5):
                    starttime = time.time()
                    sock.sendto(lastheader.bytes(),serveraddress)
                    printSending(lastheader.seqNum,"Retransmission")
                    
                #No Need to Retransmit
                if header.ackNum == lastheader.seqNum +1 : 
                    printRecieving(header.ackNum)
                    lastheader = header
                    listening = False
                    sendACK = True
        ## Change Header Values 
        if sendACK == True:
            header.ackNum = lastheader.seqNum + 1
            header.syn = 0
            header.ack = 1
            header.newSeq()
            sent = sock.sendto(header.bytes(),serveraddress)
            starttime = time.time()
            printSending(header.seqNum,"")
            if sent: 
                go = False
        
    # TERMINATE CONNECTION
    go = True
    listening = True
    sendACK = False
    lastheader = None
    seqNum = rand_int()
    finHeader = Header(seqNum, 0, 1, 0 , 0, 1)
    starttime = time.time()
    sent = sock.sendto(finHeader.bytes(),serveraddress)
    lastheader = finHeader
    if sent: 
        printSending(seqNum,"FIN")
    while go: 
        if listening: 
            data,addr = sock.recvfrom(1024)
            if data:
                header = util.decodeHeader(data)
                #Retransmission
                if header.ackNum != lastheader.seqNum + 1 or ((starttime -time.time()) > 0.5):
                    sock.sendto(lastheader.bytes(),serveraddress)
                    printSending(lastheader.seqNum,"Retransmission")
                #No Need to Retransmit
                if header.ackNum == lastheader.seqNum +1 : 
                    printRecieving(header.ackNum)
                    lastheader = header
                    listening = False
                    sendACK = True
        #Change Header Values s
        if sendACK == True:
            header.ackNum = lastheader.seqNum + 1
            header.fin = 0
            header.ack = 1
            header.newSeq()
            starttime = time.time()
            sent = sock.sendto(header.bytes(),serveraddress)
            printSending(header.seqNum,"")
            if sent: 
                go = False
if __name__ == "__main__":
    if len(sys.argv) != 3: 
        sys.exit("Usage: python simple-tcp-client.py SERVER-HOST-OR-IP PORT-NUMBER") 
    receiver_ip = sys.argv[1] 
    receiver_port = int(sys.argv[2])
    main(receiver_ip,receiver_port)
