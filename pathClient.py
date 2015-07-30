import socket,json
#todo: turn this into a module
pathSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create a socket
pathSock.connect(("localhost",7284)) # Connect to pathServer
pathSock.send("2016012246,b-Engineering 3") # Send comma-separated nodes
print json.loads(pathSock.recv(2048)) # reconstruct data