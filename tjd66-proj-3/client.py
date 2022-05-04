import socket
import sys
from util import *
import time 
class Client:
    def __init__(self,sourceNode):
        #Shortest Distance for each node 
        self.lft = {}
        #Initial Command 
        self.command = "JOIN"
        self.node = sourceNode
        #new value pairs 
        self.newvps = {}
        self.previous = {}
        #obtain list of neighbors from initial map, should never change.
        self.neighbors = []
        self.firstContact = True
    
    def initrcv(self,initvp):
        self.lft = initvp
        self.neighbors = findNeighbors(initvp,self.node)
        # on initial contact, server only sends the node pairs of each nodes neighbors... so we can set the updatedVPs to lft to forward to all neighbors
        self.updatedVPs = self.lft
        self.command = 'INITUPDATE'


    def buildMessage(self):
        m = {
            'command' : self.command,
            'node' : self.node,
            'updatedVPs' : self.newvps,
            'neighbors' : self.neighbors
        }
        return encodeData(m)


    #bellman ford algorithm 
    def bf(self):
        #Initialize 
        distance = dict.fromkeys(self.lft,float('inf'))
        distance[self.node] = 0
        for _ in range(len(self.lft) - 1):
            for v in self.lft:
                for n in self.lft[v]:
                    toCheck = self.lft[v][n]
                    #-1 means no edge connecting the two
                    if toCheck != -1:
                        distance[n] = min(distance[n], distance[v] + self.lft[v][n] )
        return distance
    
    def update(self):
        self.newvps = self.bf()
        # Keep track of previous local forwarding table to detect if any changes were made 
        self.previous = self.lft
        #Check for any changes 
        if self.change(self.node,self.newvps):
            self.lft[self.node] = self.newvps
            self.command = 'UPDATE'
        else: self.command = 'LISTENING'
    
    def rcvupdate(self,message):
        self.previous = self.lft
        updatingNode = message['node']
        updatingVPs = message['updatedVPs']
        if message['command'] == 'UPDATE' and self.change(updatingNode,updatingVPs):
            self.lft[updatingNode] = updatingVPs
            self.update()
        #If the message is an initial update... don't check for changes and just add to lft
        if message['command'] == 'INITUPDATE':
            self.lft[updatingNode] = updatingVPs
            self.update()
    
    #Check to see if any values of neighbor node has changed, return true if yes, false if no
    def change(self,updatingNode,updatingvps):
        valsToCheck = self.previous[updatingNode]
        changeVal = False
        for key, value in valsToCheck:
            if value != updatingvps[key]:
                changeVal = True
        return changeVal
                


def main(node):
    ## Host and Port Values of Server 
    HOST = '127.0.0.1'
    PORT = 55555  
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    serveraddress = (HOST,PORT)
    go = True
    client = Client(node)
    starttime = time.time()
    lastupdatetime = 0
    nochangeupdate = 0
    while go:
        #Ask to join Server 
        if client.command == 'JOIN':
            sent = sock.sendto(client.buildMessage(),serveraddress)
            if sent:
                client.command = 'LISTENING'


        #Listen for server 
        if client.command == 'LISTENING':
            rdata,addr = sock.recvfrom(1024)
            if rdata:
                r = decodeData(rdata)
                if r and client.firstContact == False:
                    client.rcvupdate(r)
                    if client.command == 'LISTENING':
                        nochangeupdate += 1
                        #If the last update time is greater than 1 minute
                        if time.time() - lastupdatetime > 60:
                            pass 
                #Client just joined, should be recieving its vps from server... then forward to its neighbors
                if r and client.firstContact == True:
                    client.initrcv(r)
                    sock.sendto(client.buildMessage(),serveraddress)
                    client.firstContact = False
            #If Client has an update send to server 

        if client.command == 'UPDATE':
            sent = sock.sendto(client.buildMessage(),serveraddress)
            if sent:
                lastupdatetime = time.time()
                client.command == 'LISTENING'

if __name__ == '__main__':
    if len(sys.argv) != 2: 
        sys.exit("Usage: python client.py [Node Value]")
    node = str(sys.argv[1])
    main(node)