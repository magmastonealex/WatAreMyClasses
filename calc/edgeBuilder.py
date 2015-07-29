from Queue import Queue
from threading import Thread
from LatLon import LatLon
import pickle
import os
from viewer import NodeCollection,Node
class edgeBuilder:
	q = Queue() # Queue because we might need it.
	nCollection=None
	def __init__(self,nodeCol): #Takes the known NodeCollection.
		self.nCollection=nodeCol

	#Builds a complete list of:
	# Node Neighbours
	# Edges of graph
	# Written in this style because it's threaded.
	def checkNode(self):
		while True:
			node=self.q.get()
			for nID2,node2 in self.nCollection.vertices.items():
				if node.id == node2.id or node2.id in node.adjacent:
					continue
				dist=node.latlong.distance(node2.latlong)*1000 #distance in km, conv to m
				dist=int(dist) # Don't need sub-meter accuracy, really.
				if dist < 40:
					self.nCollection.addEdge(node.id,node2.id,dist)
			print node.id
			self.q.task_done()

	#Create threads, add all the nodes to the queue, and run de-duplication
	#Also writes it's output to files.
	def build(self):
		for i in range(10): # Roughly falloff point of performance bell-curve on an octacore.
		     t = Thread(target=self.checkNode)
		     t.daemon = True # otherwise we need to keep track of them all. Just let them die on leave.
		     t.start()
		
		print "Running..."
		for nodeID,node in self.nCollection.vertices.items():
			self.q.put(node)
		self.q.join()

		print "De-Duplication..."
		for nodeID,node in self.nCollection.vertices.items(): #dedupe
			self.nCollection[nodeID].adjacent=list(set(node.adjacent))
