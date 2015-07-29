from Queue import Queue
from threading import Thread
from LatLon import LatLon
import pickle
import os
class edgeBuilder:
	q = Queue() # Queue because we might need it.
	def __init__(self,edges=[],ngraph=[],nodes={}): #Optionally takes basic edges, basic graph, and all the known nodes. 
		self.edges=edges
		self.ngraph=ngraph
		self.nodes=nodes
	#Builds a complete list of:
	# Node Neighbours
	# Edges of graph
	# Written in this style because it's threaded.
	def checkNode(self):
		while True:
			node,idx=self.q.get()
			nLL=node["ll"]
			for node2 in self.ngraph:
				if node["id"] == node2["id"] or node2["id"] in node["neighbours"]:
					continue
				n2LL=node2["ll"]
				dist=nLL.distance(n2LL)*1000 #distance in km, conv to m
				dist=int(dist) # Don't need sub-meter accuracy, really.
				if dist < 40:
					self.edges.append([node["id"],node2["id"],dist])
					self.ngraph[idx]["neighbours"].append(node2["id"])
					self.ngraph[self.ngraph.index(node2)]["neighbours"].append(node["id"])
			q.task_done()

	#Don't care how, but make the data valid for use.
	def makeDataValid(self):
		if self.canLoad():
			self.load()
		else:
			self.build()
	#Check if the class has enough info already written to initialize itself. 
	def canLoad(self):
		if os.path.exists("graph.pic"):
			return True
		else:
			return False
	#Create threads, add all the nodes to the queue, and run de-duplication
	#Also writes it's output to files.
	def build(self):
		for i in range(10): # Roughly falloff point of performance bell-curve on an octacore.
		     t = Thread(target=self.checkNode)
		     t.daemon = True # otherwise we need to keep track of them all. Just let them die on leave.
		     t.start()
		print "Running..."
		for node in self.ngraph:
			self.q.put([node,ngraph.index(node)])
		self.q.join()
		print "De-Duplication..."
		for node in self.ngraph: #de-duplication
			self.ngraph[self.ngraph.index(node)]["neighbours"]=list(set(node["neighbours"]))
		pickle.dump(self.ngraph,open("graph.pic","wb"))
		pickle.dump(self.edges,open("edges.pic","wb"))
	#Load all the data from files.
	def load(self):
		print "Loading calculated values"
		self.ngraph=pickle.load(open("graph.pic","rb"))
		self.edges=pickle.load(open("edges.pic","rb"))
		print "Loaded calculated values"