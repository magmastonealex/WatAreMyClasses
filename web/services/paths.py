import socket,json
from db import Database
import json
"""
Client class for PathServer microservice
Gets path between any two known nodes.
Init by passing a Database object.

Run getPath(nodeid1,nodeid2) to have a path returned.

Heavily utilizes caching via Redis..
"""
class Paths:
	def __init__(self,db):
		self.db=db
	def getPath(self,u,v):
		dbpath=db.redis_get("path:"+u+":"+v)
		if dbpath != None:
			return json.loads(dbpath)
		else:
			pathSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket
			pathSock.connect(("localhost",7284)) # Connect to pathServer
			pathSock.send(u+","+v) # Send comma-separated nodes
			jsn=pathSock.recv(2048)
			x=json.loads(jsn)
			pathSock.close()
			db.redis_set("path:"+u+":"+v,jsn)
			return x