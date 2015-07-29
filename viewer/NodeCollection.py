import pickle

class Node(object):
	def __init__(self,container,ID,x,y,adjacent=[],name='',latlong=None):
		self.container=container
		self.id=ID
		self.x=x
		self.y=y
		self.adjacent=adjacent		#list of (nodeID,distance to node) pairs
		self.name=name				#string
		self.latlong=latlong

class NodeCollection(object):
	"""General-purpose collection class for nodes.
	Sample usage:
	>>nodes=NodeCollection()
	>>nodes.addNode(1,  100, 200, name='first!')
	                id, x,   y,   convenient keyword argument
	>>nodes.addNode(2, 200, 100, name='second')
	>>nodes.addEdge(1,2,300)	#adds an edge of length 300 between nodes WIDTHh ID 1 and 2
	"""

	def __init__(self):
		self.vertices={}
		self.edges=[]

	def __getitem__(self,k):
		return self.vertices[k]

	def addNode(self,ID,*args,**kwargs):
		self.vertices[ID]=Node(self,ID,*args,**kwargs)

	def addEdge(self,id1,id2,length):
		self.vertices[id1].adjacent.append((id2,length))
		self.vertices[id2].adjacent.append((id1,length))
		self.edges.append((min(id1,id2),max(id1,id2),length))
	def save(self):
		pickle.dump(self.vertices,open("verts.pic","wb"))
		pickle.dump(self.edges,open("edges.pic","wb"))
	def load(self):
		self.vertices=pickle.load(open("verts.pic","rb"))
		self.edges=pickle.load(open("edges.pic","rb"))
	def dedupe(self):
		self.edges=list(set(self.edges))
def ccw(a,b,c):
    return (b.x - a.x)*(c.y - a.y) - (b.y - a.y)*(c.x - a.x)

def transform(x, y, scale, camerax, cameray):
	#returns (x,y) when scaled by transformed
	return int(scale*(x-camerax))+WIDTH/2, int(scale*(y-cameray))+HEIGHT/2