## Imports 
import datetime
import signal
import socket
import sys
import time
import util
import pickle
from util import printRecieving, printSending
# Methods 

def udpSocket(ack_port):
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #UDP
    send_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    send_sock.bind(("", ack_port))
    return send_sock

def tcpSocket(ack_port):
    ack_sock = socket.socket()
    ack_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ack_sock.bind(("", ack_port))
    ack_sock.listen(1)
    return ack_sock

def threeWayHandshake(socket):
    con = (socket.accept()[0])
    connection = False
    while connection != True:
        data = con.recv(1024)
        obj = pickle.loads(data)
        del data
        obj.Connection()
        con.sendall(pickle.dumps(obj))
        connection = obj.IsConnected()
    con.close()




## Main Method 
if __name__ == '__main__':
    ## Take Initial Arguments 
    ##Use Try Except 
    port = sys.argv[1]

    # Intialization of variables 
    seqnum = 0
    acknum = 0
    final = False 
    sent = 0
    retransmitted = 0
    tcp_established = False
    timeout_time = 0.5 #(500 milliseconds)

    # Create sockets
    try:
        send_sock = udpSocket(ack_port)
        tcp_sock = tcpSocket(ack_port)
    except socket.error:
        exit('Error while creating Socket.')

    