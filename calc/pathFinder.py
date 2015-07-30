import pickle
import os
#Loads/calculates needed data for pathfinding.
from viewer import NodeCollection,Node
class pathFinder:
	dist=[]
	nex=[]
	edges=[]
	nodeCol=None
	#Optionally takes in a list of edges. Not needed if the files are computed already.
	def __init__(self,nC):
		self.nodeCol=nC

	#Uses Floyd-Warshall algorithm to build distances between nodes, as well as a "next node" dictionary for use in pathfinding.
	#Saves it's output to be loaded next time.
	def build(self): #number of edges,
		edgeU=self.nodeCol.edges
		edges=[]
		for edge in edgeU:
			edges.append(edge)
			edges.append((edge[1],edge[0],edge[2]))

		print "Starting calculation..."

		print len(edges)
		#dist=[[INF]*V for i in range(V)]
		dist={}
		nex={}
		#init dist dictionary. I'm pretty sure that this will have the side effect of removing any dupes.
		for edge in edges:
			dist[edge[0]]={}
			nex[edge[0]]={}
			for ed in edges:
				if ed[0] != edge[0]:
					dist[edge[0]][ed[0]]=10**10 #INF!
					nex[edge[0]][ed[0]]=ed[0]
		print "Initted"
		#distance to self always =0
		for i in edges:
			dist[i[0]][i[0]] = 0
		#Set already-known distances
		for (start,end,distance) in edges:
			dist[start][end] = distance

		#Calculate distances for the rest
		cnt=0
		for k in edges:
			k=k[0]
			print k
			print cnt
			cnt=cnt+1
			for j in edges:
				j=j[0]
				for i in edges:
					i=i[0]
					if dist[i][j] > dist[i][k] + dist[k][j]:
						dist[i][j] = dist[i][k] + dist[k][j]
						nex[i][j] = nex[i][k]
		self.dist=dist
		self.nex=nex
		print "Finished!"

		print "De-Dupe complete"
		pickle.dump(self.dist,open("dist.pic","wb"))
		pickle.dump(self.nex,open("nex.pic","wb"))

	#Load all the files.
	def load(self):
		self.dist=pickle.load(open("dist.pic","rb"))
		self.nex=pickle.load(open("nex.pic","rb"))
	
	#findPath is used to find the ideal path between two nodes.
	#distance is easy: self.dist[u][v]
	#Pass in two node IDs.
	def findPath(u,v):
		if self.nex[u][v]==None:
			return []
		path = [u]
		while u != v:
			u=self.nex[u][v]
			path.append(u)
		return path