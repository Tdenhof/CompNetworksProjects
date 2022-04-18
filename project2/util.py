import socket
import struct

def printSending(seq,arg):
    if arg == 1:
        send = " Retransmission"
    if arg == 2:
        send = " SYNACK"
    if arg == 3:
        send = " FIN"
    print("Sending Packet " + seq + send)
def printRecieving(ack):
    print("Recieving " + ack)

def make_packet(source_port, dest_port, seqnum, acknum, ack, final, window_size, contents):
    if ack:
        flags +=
