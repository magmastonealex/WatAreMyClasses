import socket,json

class Paths:
	def getPath(self,u,v):
		pathSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket
		pathSock.connect(("localhost",7284)) # Connect to pathServer
		pathSock.send(u+","+v) # Send comma-separated nodes
		x=json.loads(pathSock.recv(2048))
		pathSock.close()
		return x