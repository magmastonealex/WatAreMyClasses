import socket,json

def paths:
	def getPath(self,u,v):
		pathSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket
		pathSock.connect(("localhost",7284)) # Connect to pathServer
		pathSock.send("2016012246,b-Engineering 3") # Send comma-separated nodes
		pathSock.shutdown()
		pathSock.close()
		return json.loads(pathSock.recv(2048))