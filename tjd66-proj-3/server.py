
import pandas as pd
import sys
import util
import socket
import types
import selectors
# import thread module
from _thread import *
import threading
import time


host = '127.0.0.1'
port = 55555   

class server:
    def __init__(self,initmap):
        #map from config file 
        self.initmap = initmap
        #network map
        self.nmap = {}
        #value pair map 
        self.unchangedCounter = dict.fromkeys(initmap,0)
        self.unchangedBool = dict.fromkeys(initmap,False)

        self.vpmap = initmap
        self.state = 'WAITING'
        self.nodesPresent = self.createNodeList(initmap)
    def createNodeList(self,initmap):
        nodesPresent = {}
        for key in initmap:
            nodesPresent[key] = False
        return nodesPresent
    def join(self,newNode,addr):
        if newNode in self.initmap.keys():
            #SET Current Map Values upon join
            self.nodesPresent[newNode] = True
            self.nmap[newNode] = {
                'addr' : addr,
                'nodePairs' : self.initmap[newNode]
            }
            return True
        else: return False 
    def allNodesPresent(self):
        for key in self.nodesPresent.keys():
            if self.nodesPresent[key] == False:
                return False
        return True
    #Depending on whatever node, send the init local forwarding table
    #initlft includes only value pairs that correspond to the node ID... Otherwise, set to inf
    def createinitlft(self,node):
        newdic = {}
        for key in self.initmap.keys():
            newdic[key] = dict.fromkeys(self.initmap,float('inf'))
        newdic[node] = self.initmap[node]
        returndic = {
            'command' : 'initVP',
            'initlft' : newdic
        } 
        return returndic

def buildMessage(r):
    return util.encodeData(r)

def main(configFile):
    initmap = util.load_config(configFile)
    serv = server(initmap)
    print('Initial Graph')
    print(initmap)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket 
    sock.bind((host,port))
    print('waiting for clients to connect...')
    lastupdate = None
    go = True
    while go:
        if serv.state == 'Kill-update.final':
            for node in serv.nmap.keys():
                s = util.encodeData(serv.state)
                sock.sendto(s, serv.nmap[node]['addr'])
                go = False
        rdata, addr = sock.recvfrom(1024)
        if not rdata:
            continue
        else:
            r = util.decodeData(rdata)
            # Check JOIN 
            if r['command'] == 'JOIN':
                newnode = r['node']
                joined = serv.join(newnode,addr)
                if joined: 
                    print('Node ' + r['node'] + ' joined from address ' + str(addr))
                    print('Connected Clients: ' + str(serv.nmap))
                    
                else:
                    s = util.encodeData('KILL-node.error')
                    sock.sendto(s,addr)
            
            if serv.allNodesPresent() and serv.state != 'OPERATIONAL':
                serv.state = 'OPERATIONAL'
                for node in serv.nmap.keys():
                    s = util.encodeData(serv.createinitlft(node))
                    sock.sendto(s, serv.nmap[node]['addr'])
            
            #UPDATE FUNCTION -- node can only read update if connection is verified by JOIN... no need to check if r[node] in keys
            if r['command'] == 'UPDATE':
                lastupdate = time.time()
                print(str(r['command']) + ' from ' + str(r['node']) + str(r['updatedVPs']) + ' to ' + str(r['neighbors']))
                #Add to Update Counter 
                if serv.nmap[r['node']]['nodePairs'] == r['updatedVPs']:
                    serv.unchangedCounter[r['node']] += 1
                    #If all keys havent changed in 3 updates
                    a_boolean = all(counter > 3 for counter in serv.unchangedCounter.values())
                    if a_boolean == True: 
                        serv.state = 'Kill-update.final'
                #Update server nodepair values 
                serv.nmap[r['node']]['nodePairs'] = r['updatedVPs']
                

                # loop through the neighbors of the update node and pass on message 
                for neighbor in r['neighbors']:
                    address = serv.nmap[neighbor]['addr']
                    sock.sendto(rdata,address)
                    print('Forwarded update from ' + str(r['node']) + ' to ' + str(neighbor) + ' at address ' + str(address))
    sock.close()
    print(serv.nmap)

if __name__ == '__main__':
        if len(sys.argv) != 2: 
            sys.exit("Usage: python server.py [config_file_path]")
        configFile = sys.argv[1]
        configFile = str(configFile)
        main(configFile)
                    





