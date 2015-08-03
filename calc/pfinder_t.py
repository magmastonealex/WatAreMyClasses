import pickle
import os
import threading
import subprocess
#Loads/calculates needed data for pathfinding.

from viewer import NodeCollection,Node
"""
Uses a C helper to very quickly compute the Floyd-Warshall algorthm. Takes ~ 10 mins.
Only needed during cache-prep.
"""

class pathFinder_Threaded:
	dist=[]
	nex=[]
	nodeCol=None
	#Optionally takes in a list of edges. Not needed if the files are computed already.
	def __init__(self,nC):
		self.nodeCol=nC

	#Uses Floyd-Warshall algorithm to build distances between nodes, as well as a "next node" dictionary for use in pathfinding.
	#Saves it's output to be loaded next time.
	def build(self,**kwargs): #number of edges,
		edgeU=self.nodeCol.edges
		edges=[]
		dist={}
		nex={}
		print len(self.nodeCol.vertices)
		cur_node=0
		nodes_mapping={}
		nodes_inverse={}
		for edge in edgeU:
			e1=0
			e2=0
			# OSM may dump extra nodes into nodeCollection. No point in processing them, also may cause segfaults.
			if edge[0] not in nodes_mapping:
				nodes_mapping[edge[0]]=cur_node
				nodes_inverse[cur_node]=edge[0]
				e1=cur_node
				cur_node=cur_node+1
			else:
				#print "mtched"
				e1=nodes_mapping[edge[0]]

			if edge[1] not in nodes_mapping:
				nodes_mapping[edge[1]]=cur_node
				nodes_inverse[cur_node]=edge[1]
				e2=cur_node
				cur_node=cur_node+1
			else:
				#print "mtched"
				e2=nodes_mapping[edge[1]]

			if edge[0]=="1928136290" and edge[1]=="1932767863":
				print "shouldbe: "+str(e1)+"->"+str(e2)
#			print edge[0]+"<->"+edge[1]
			edges.append((e1,e2,edge[2]))
			edges.append((e2,e1,edge[2]))
		for edge in edges:
			if edge[0]==109 and edge[1]==2:
				print "inere"
		fout1=open("cimp/emaps.csv","w")
		for nid,new in nodes_mapping.items():
			fout1.write(nid+"->"+str(new)+"\n")
		fout1.close()
		print "Writing data for C..."
		fout=open("cimp/data.csv","w")
		fout.write(str(cur_node)+"\n")
		for edge in edges:
			fout.write(str(edge[0])+","+str(edge[1])+","+str(int(edge[2]))+"\n")
		fout.close()

		#raw_input("Please run the C program and press enter here to continue processing") # Python's subprocess.call observably wastes resources. 
		os.chdir("cimp")
		subprocess.call(["./out"])
		os.chdir("..")

		fin=open("cimp/dataout.csv","r")
		c_n1=0
		for line in fin.readlines():
			dist[nodes_inverse[int(c_n1)]]={}
			line=line.rstrip()[1:]
			dat=line.split(",")
			c_n2=0
			for x in dat:
				n,d=x.split("-")
				dist[nodes_inverse[int(c_n1)]][nodes_inverse[int(c_n2)]]=int(d)
				c_n2=c_n2+1
			c_n1=c_n1+1
		fin.close()
		fin=open("cimp/dataout-nex.csv","r")
		c_n1=0
		for line in fin.readlines():
			nex[nodes_inverse[int(c_n1)]]={}
			line=line.rstrip()[1:]
			dat=line.split(",")
			c_n2=0
			for x in dat:
				n,d=x.split("-")
				if c_n2==c_n1:
					c_n2=c_n2+1
					continue
				nex[nodes_inverse[int(c_n1)]][nodes_inverse[int(c_n2)]]=nodes_inverse[int(d)]
				c_n2=c_n2+1
			c_n1=c_n1+1
		fin.close()
		self.dist=dist
		self.nex=nex

		print "Finished!"
		#dedupe based on the same characteristics as NodeController does for Edges.
		print "De-Dupe complete"
		if "test" not in kwargs:
			pickle.dump(self.dist,open("dist.pic","wb"))
			pickle.dump(self.nex,open("nex.pic","wb"))

	#Load all the files.
	def load(self):
		self.dist=pickle.load(open("dist.pic","rb"))
		self.nex=pickle.load(open("nex.pic","rb"))
	
	#findPath is used to find the ideal path between two nodes.
	#distance is easy: self.dist[u][v]
	#Pass in two node IDs.
	def findPath(self,u,v):
		if self.nex[u][v]==None:
			return []
		path = [u]
		while u != v:
			u=self.nex[u][v]
			path.append(u)
		return path