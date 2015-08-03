import pickle

class Node(object):
	def __init__(self,ID,x,y,name='',latlong=None):
		self.id=str(ID)
		self.x=float(x)
		self.y=float(y)
		self.adjacent={}		#list of (nodeID,distance to node) pairs
		self.name=str(name)				#string
		self.latlong=latlong

	def data(self):
		"""returns initialization arguments necessary to create identical node. Any edges are not copied."""
		return (self.id, self.x, self.y, self.name)

class NodeCollection(object):
	"""General-purpose collection class for nodes.
	Sample usage:
	>>nodes=NodeCollection()
	>>nodes.addNode(1,  100, 200, 'first!')
	                id, x,   y,   convenient keyword argument
	>>nodes.addNode(2, 200, 100, 'second')
	>>nodes.addEdge(1,2,300)	#adds an edge of length 300 between nodes with ID 1 and 2
	"""

	def __init__(self):
		self.vertices={}
		self.edges=[]

	def __getitem__(self,k):
		return self.vertices[k]

	def addNode(self,ID,*args,**kwargs):
		self.vertices[str(ID)]=Node(str(ID),*args,**kwargs)

	def addEdge(self,id1,id2,length):
		self.vertices[str(id1)].adjacent[str(id2)] = length
		self.vertices[str(id2)].adjacent[str(id1)] = length
		L=sorted([str(id1),str(id2)])
		self.edges.append((L[0],L[1],length))

	def getSaveString(self):
		"""Returns a string which can be loaded is what WOULD be written to file"""
		s=""
		s+=(str(len(self.vertices.keys()))+"\n")
		for key in sorted(self.vertices.keys()):
			s+=("|".join(map(str,self[key].data()))+"\n")
		s+=(str(len(self.edges))+"\n")
		for edge in sorted(sorted(sorted(self.edges,key=lambda l:l[0]),key=lambda l:l[1]),key=lambda l:l[2]):
			s+=("|".join(map(str,edge))+"\n")
		return s

	def save(self, filename):
		"""Non-destructively writes itself to said file. File format:
			N 			number of vertices
			the next N lines have the form id|x|y|name

		does not currently save LatLon information
		"""
		f=file(filename,"w")
		f.write(self.getSaveString())
		f.close()

	def loadFromSaveString(self, inp):
		"""clears self, then loads from a string."""
		NodeCollection.__init__(self)	#wipes old data
		inp=inp.split("\n")

		numNodes=int(inp[0])
		for n in range(numNodes):
			data=inp[n+1].split("|",3)

			data=data[0],float(data[1]),float(data[2]),data[3]
			self.addNode(*data)

		numEdges=int(inp[numNodes+1])
		for n in range(numEdges):
			data=inp[n+2+numNodes].split("|")
			data=data[0], data[1],float(data[2])
			self.addEdge(*data)

	def load(self, filename):
		"""file wrapper for loadFromSaveString"""
		f=file(filename,"r")
		self.loadFromSaveString(f.read())
		f.close()

	def dedupe(self):
		self.edges=list(set([(min(edge[0],edge[1]),max(edge[0],edge[1]),edge[2])for edge in self.edges]))
	
def ccw(a,b,c):
	return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)
