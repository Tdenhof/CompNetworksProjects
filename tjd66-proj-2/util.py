import socket
import struct
from enum import Enum
import random


def printSending(seq,type):
    print("Sending Packet " + str(seq) +' '+ type)
def printRecieving(ack):
    print("Recieving " + str(ack))

#Header Class 
class Header:
    #Constructor
    def __init__(self,seqNum,ackNum,win,ack,syn,fin):
        #ack,syn,fin (1 --> True, 0 --> False)
        self.seqNum = seqNum
        self.ackNum = ackNum
        self.win = win
        self.syn = syn 
        self.ack = ack
        self.fin = fin
        self.NotUsed = 0
    def newSeq(self):
        go = True
        while go:
            r = rand_int()
            if r != self.seqNum:
                go = False
        self.seqNum = r
    def newACK(self):
        self.ackNum = self.seqNum + 1
        self.newSeq()
        self.ack = 1
    def endAck(self):
        self.ackNum = self.seqNum + 1
        self.newSeq()
        self.ack = 1
        self.syn = 0
    #to Bit representation
    def bytes(self):
        #{0:0x} --> x = number of bites
        bits = '{0:016b}'.format(self.seqNum)
        bits += '{0:016b}'.format(self.ackNum)
        bits += '{0:016b}'.format(self.win)
        bits += '{0:013b}'.format(self.NotUsed)
        bits += '{0:01b}'.format(self.ack)
        bits += '{0:01b}'.format(self.syn)
        bits += '{0:01b}'.format(self.fin)
        bits.encode()
        # 64 total bites --> 8 bytes fixed
        return bits.encode()

#Return header values from packet 
def decodeHeader(bits):
    seqNum = int(bits[:16], 2)
    ackNum = int(bits[16:32], 2)
    win = int(bits[32:48],2)
    ack = int(bits[61:62],2)
    syn = int(bits[62:63], 2)
    fin = int(bits[63:64],2)
    return Header(seqNum,ackNum,win,ack,syn,fin)

#Helper Method for seqNum
def rand_int():
    go = True
    while go:
        r = random.randint(0,(2 ** 5)-1)
        ## MAX SEQ NUM SIZE
        if r < 30720:
            go = False
    return r 
