import socket 
import util
from util import *
import sys
IP = "127.0.0.1"
listening = False
synRecieved = False
synSent = False

def recv(sock):
    data,addr = sock.recv(1024)
    header = util.decodeHeader(data)
    content = util.getContent(data)
    printRecieving(header.ackNum)
    return(header,content,addr)

# Implement Sending back to client 
# def sendv(sock):

def main(serverPort):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket 
    sock.bind((IP, serverPort))
    go = True
    while go:
        # check if listening 
        if not listening: 
            listening = True

        elif listening:
            header, content, addr = recv(sock)
            # syn = true
            # if syn = true --> Connection
            if header.syn == 1: 
                header.seqNum = header.seqNum + 1
                ## implement sending back to client 
        elif synRecieved:
            pass
        elif synSent:
            pass
        else:
            pass

if __name__ == '__main__':
    if len(sys.argv) != 2: 
        sys.exit("Usage: python simple-tcp-server.py [PORT-NUMBER]")
    portN = sys.argv[1]
    serverPort = int(portN)
    main(serverPort)
