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
        self.neighborUpdates = {}
    
    def initrcv(self,initvp):
        self.lft = initvp
        # on initial contact, server only sends the node pairs of each nodes neighbors... so we can set the updatedVPs to lft to forward to all neighbors
        self.updatedVPs = self.lft
        


    def buildMessage(self):
        m = {
            'command' : self.command,
            'node' : self.node,
            'updatedVPs' : self.newvps,
            'neighbors' : self.neighbors,
            'neighborUpdates' : self.neighborUpdates
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
        # Keep track of previous local forwarding table to detect if any changes were made 
        self.previous = self.lft
        updates = self.bf()
        #Check for any changes 
        self.lft[self.node] = updates
        self.newvps = updates
        #If there is a change, forward to the neighbor nodes 
        self.command = 'UPDATE'
        
    
    def rcvupdate(self,message):
        self.previous = self.lft
        if message['command'] == 'initVP':
            self.lft = message['initlft']
            self.neighbors = findNeighbors(self.lft,self.node)
            self.update()
        else:
            updatingNode = message['node']
            updatingVPs = message['updatedVPs']
            #If the message Command is update, and theres changes from the update to what the current lft is, then update our lft 
            if message['command'] == 'UPDATE':
                self.neighborUpdates[updatingNode] = updatingVPs
                self.lft[updatingNode] = updatingVPs
                self.update()
        #If the message is an initial update... don't check for changes and just add to lft

    
    #Check to see if any values of neighbor node has changed, return true if yes, false if no
    def change(self,updatingNode,updatingvps):
        valsToCheck = self.previous[updatingNode]
        changeVal = False
        for key in valsToCheck.keys():
            if valsToCheck[key] != updatingvps[key]:
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
    while go:
        #Ask to join Server 
        if client.command == 'JOIN':
            sock.sendto(client.buildMessage(),serveraddress)
            client.command = 'LISTENING'

        #Listen for server 
        if client.command == 'LISTENING':
            rdata,addr = sock.recvfrom(1024)
            if rdata:
                r = decodeData(rdata)
                if r == 'Kill-node.error':
                    go = False
                    print('Router Killed because no node ' + client.node +' exists in server process')
                elif r == 'Kill-update.final':
                    print(client.lft)
                    go = False
                else: client.rcvupdate(r)

        if client.command == 'UPDATE':
            sock.sendto(client.buildMessage(),serveraddress)
            client.command = 'LISTENING'
    sock.close()
    
if __name__ == '__main__':
    if len(sys.argv) != 2: 
        sys.exit("Usage: python client.py [Node Value]")
    node = str(sys.argv[1])
    main(node)