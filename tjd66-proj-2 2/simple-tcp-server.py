import socket 
import util
from util import *
import sys
import time



def main(serverPort):
    IP = "127.0.0.1"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket 
    sock.bind((IP,serverPort))
    go = True
    # ESTABLISH CONNECTION
    listening = False
    sendSYNACK = False
    lastheader = None
    initialListen = True
    while go:
        if initialListen: 
            data,addr = sock.recvfrom(1024)
            if data:
                header = util.decodeHeader(data)
                printRecieving(header.ackNum)
                initialListen = False
                sendSYNACK = True
                lastheader = header
        # check if listening 
        if listening: 
            data,addr = sock.recvfrom(1024)
            if data: 
                header = util.decodeHeader(data)
                ## Retransmission
                if header.ackNum != lastheader.seqNum + 1 or (starttime - time.time() > 0.5):
                    sock.sendto(lastheader.bytes(),addr)
                    printSending(lastheader.seqNum,"Retransmission")
                #No need to retransmit
                if header.ackNum == lastheader.seqNum + 1:
                    printRecieving(header.ackNum)
                    if header.syn == 0:
                        go = False
                        listening = False
                        sendSYNACK = False
                    if header.syn == 1:
                        listening = False
                        sendSYNACK = True
                    lastheader = header 
        #Change Header Values 
        if sendSYNACK == True:
            header.ackNum = lastheader.seqNum + 1
            header.syn = 1
            header.newSeq()
            starttime = time.time()
            sent = sock.sendto(header.bytes(),addr)
            printSending(header.seqNum,"SYNACK")
            if sent: 
                sendSYNACK = False
                listening = True
        else:
            pass
    ## TERMINATE CONNECTION 
    listening = False
    sendFINACK = False
    go = True
    lastheader = None
    initialListen = True
    while go:
        # check if listening 
        if initialListen: 
            data,addr = sock.recvfrom(1024)
            if data:
                header = util.decodeHeader(data)
                printRecieving(header.ackNum)
                initialListen = False
                sendFINACK = True
                lastheader = header
        if listening: 
            data,addr = sock.recvfrom(1024)
            if data: 
                header = util.decodeHeader(data)
                #RETRANSMISSION
                if header.ackNum != lastheader.seqNum + 1 or (starttime - time.time() > 0.5):
                    sock.sendto(lastheader.bytes(),addr)
                    printSending(lastheader.seqNum,"Retransmission")
                #NO NEED TO RETRANSMIT
                if header.ackNum == lastheader.seqNum +1 :
                    printRecieving(header.ackNum)
                    if header.fin == 0:
                        go = False
                        listening = False
                        sendFINACK = False
                    if header.fin == 1:
                        listening = False
                        sendFINACK = True
                    lastheader = header 
        #Change Header Values 
        if sendFINACK == True:
            header.ackNum = lastheader.seqNum + 1
            header.fin = 1
            header.newSeq()
            starttime = time.time()
            sent = sock.sendto(header.bytes(),addr)
            printSending(header.seqNum,"FIN")
            if sent: 
                sendFINACK = False
                listening = True
        else:
            pass
if __name__ == '__main__':
    if len(sys.argv) != 2: 
        sys.exit("Usage: python simple-tcp-server.py [PORT-NUMBER]")
    portN = sys.argv[1]
    serverPort = int(portN)
    main(serverPort)
