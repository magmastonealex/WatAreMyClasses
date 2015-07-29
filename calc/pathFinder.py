import pickle

#Loads/calculates needed data for pathfinding.

class pathFinder:
	dist=[]
	nex=[]
	edges=[]
	#Optionally takes in a list of edges. Not needed if the files are computed already.
	def __init__(self,ledges=None):
		if ledges==None:
			self.edges=ledges

	#Uses Floyd-Warshall algorithm to build distances between nodes, as well as a "next node" dictionary for use in pathfinding.
	#Saves it's output to be loaded next time.
	def build(edges): #number of edges,
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
		#distance to self always =0
		for i in edges:
			dist[i[0]][i[0]] = 0
		#Set already-known distances
		for (start,end,distance) in edges:
			dist[start][end] = distance
		#Calculate distances for the rest
		for k in edges:
			k=k[0]
			for j in edges:
				j=j[0]
				for i in edges:
					i=i[0]
					if dist[i][j] > dist[i][k] + dist[k][j]:
						dist[i][j] = dist[i][k] + dist[k][j]
						nex[i][j] = nex[i][k]
		self.dist=dist
		self.nex=nex
		pickle.dump(self.dist,open("dist.pic","wb"))
		pickle.dump(self.nex,open("nex.pic","wb"))

	#Call this to either build or load all of the data needed for pathfinding.
	def makeDataValid():
		if self.canLoad():
			self.load()
		else:
			if self.edges==[]:
				raise NeedCalculationDataError
			self.build(self.edges)
			
	#Check if the class has all the files it needs to load.
	def canLoad(self):
		if os.path.exists("dist.pic"):
			return True
		else:
			return False
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