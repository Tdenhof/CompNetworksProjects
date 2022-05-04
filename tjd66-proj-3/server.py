from json import load
from turtle import update
import pandas as pd
import sys
import util
import socket
import types
import selectors
# import thread module
from _thread import *
import threading


host = '127.0.0.1'
port = 55555   

class server:
    def __init__(self,initmap):
        #map from config file 
        self.initmap = initmap
        #network map
        self.nmap = {}
        #value pair map 
        self.vpmap = initmap
        self.state = 'WAITING'
        self.nodesPresent = self.createNodeList(initmap)
    def createNodeList(self,initmap):
        nodesPresent = {}
        for key in initmap:
            nodesPresent[key] = False
    def join(self,newNode,addr):
        if newNode in self.initmap.keys():
            #SET Current Map Values upon join
            self.nodesPresent[newNode] = True
            self.nmap[newNode] = {
                'addr' : addr,
                'nodePairs' : self.initmap[newNode]
            }
    def allNodesPresent(self):
        for key, value in self.nodesPresent:
            if value == False:
                return False
        return True
    #Depending on whatever node, send the init local forwarding table
    #initlft includes only value pairs that correspond to the node ID... Otherwise, set to inf
    def createinitlft(self,node):
        newdic = {}
        for key in self.initmap.keys():
            newdic[key] = dict.fromkeys(self.initmap,float('inf'))
        newdic[node] = self.initmap[node]
        return newdic

def buildMessage(r):
    return util.encodeData(r)

def main(configFile):
    initmap = util.load_config(configFile)
    serv = server(initmap)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP socket 
    sock.bind((host,port))
    while True:
        rdata, addr = sock.recvfrom(1024)
        if not rdata:
            continue
        else:
            r = util.decodeData(rdata)
            # Check JOIN 
            if r['command'] == 'JOIN':
                newnode = r['node']
                serv.join(newnode,addr)
                print('Node ' + r['node'] + ' joined from address ' + str(addr))
            if serv.state == 'WAITING':
                if serv.allNodesPresent():
                    serv.state == 'OPERATIONAL'
                    for node in serv.nmap.keys():
                        s = util.encodeData(serv.createinitlft(node))
                        sock.sendto(s, serv.nmap[node]['addr'])
            
            #UPDATE FUNCTION -- node can only read update if connection is verified by JOIN... no need to check if r[node] in keys
            if r['command'] == 'UPDATE' and serv.state == 'OPERATIONAL':
                #Update server nodepair values 
                serv.nmap[r['node']]['nodePairs'] = r['updatedVPs']
                # loop through the neighbors of the update node and pass on message 
                for neighbor in r['neighbors']:
                    address = serv.nmap[neighbor]['addr']
                    sent = sock.sendto(buildMessage(r),address)
                    if sent:
                        print('Forwarded update from ' + r['node'] + ' to ' + neighbor)
            


if __name__ == '__main__':
        if len(sys.argv) != 2: 
            sys.exit("Usage: python server.py [config_file_path]")
        configFile = sys.argv[1]
        configFile = str(configFile)
        main(configFile)
                    





