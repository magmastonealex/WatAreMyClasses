"""
This serves paths to the web side. It allows all of the path data to be kept in memory,
without loading it into Python types from files or network, which is very slow
Protocol:
	- exaple in pathClient.py
	- 1. Connect, send comma-separated two nodes
	- 2. Receive JSON array back. Array contains the nodes, in order, for the path.
"""

from socket import *
import thread
from calc import pathFinder
import redis
import json

BUFF = 1024
HOST = '127.0.0.1'
PORT = 7284 # PATH :)

cache=redis.Redis()

pF = pathFinder(None)
pF.load()

def read_socket(client):
	return client.recv(1)

def handler(clientsock,addr):
	global cache
	global pF
	
	data = clientsock.recv(1024)
	print data.decode("ascii")
	data=data.decode("ascii").rstrip()
	if not data: 
		clientsock.close()
		return
	nodes=data.split(",")
	clientsock.send(json.dumps(pF.findPath(nodes[0],nodes[1])))
	clientsock.close()
 
if __name__=='__main__':

	serversock = socket(AF_INET, SOCK_STREAM)
	serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
	serversock.bind((HOST, PORT))
	serversock.listen(20)
	while 1:
		print "Started"
		clientsock, addr = serversock.accept()
		print '...connected from:', addr
		thread.start_new_thread(handler, (clientsock, addr))
