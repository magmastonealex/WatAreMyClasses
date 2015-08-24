import pickle
import os
import threading
import subprocess
import array
#Loads/calculates needed data for pathfinding.

from viewer import NodeCollection,Node
"""
Uses a C helper to very quickly compute the Floyd-Warshall algorthm. Takes ~ 10 mins.
Only needed during cache-prep

Use:
x= pathFinder_Threaded(nodeCollection) - initalize with a nodeCollection to build paths of.

x.build() - Build & save it. Passing test=True prevents saving  (used in unit-tests)

x.load() - Loads data. Prevents the need to call build() every time.

x.findPath(nd1,nd2) - Find the most efficient path between two nodes. Returns an array of node IDs.



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
			fout1.write(nid+";"+str(new)+"\n")
		fout1.close()
		print "Writing data for C..."
		fout=open("cimp/data.csv","w")
		fout.write(str(cur_node)+"\n")
		for edge in edges:
			fout.write(str(edge[0])+","+str(edge[1])+","+str(int(edge[2]))+"\n")
		fout.close()
		self.nodes_map=nodes_mapping
		self.nodes_inv=nodes_inverse
		#raw_input("Please run the C program and press enter here to continue processing") # Python's subprocess.call observably wastes resources. 
		os.chdir("cimp")
		subprocess.call(["./out"])
		os.chdir("..")
		#fin=open("cimp/dataout.csv","r")
		#dist=[]
		#nex=[]
		#c_n1=0
		#for line in fin.readlines():
		#	#dist[nodes_inverse[int(c_n1)]]={}
		#	tmp=array.array("I")
		#	line=line.rstrip()[1:]
		#	dat=line.split(",")
		#	c_n2=0
		#	for x in dat:
		#		n,d=x.split("-")
		#		#dist[nodes_inverse[int(c_n1)]][nodes_inverse[int(c_n2)]]=int(d)
		#		tmp.append(int(d))
		#		c_n2=c_n2+1
		#	c_n1=c_n1+1
		#	dist.append(tmp)
		#	print "dst="+str(c_n1)
		#fin.close()
		#del dist
		##pickle.dump(dist,open("dist.pic","wb"))
		#
		#fin=open("cimp/dataout-nex.csv","r")
		#c_n1=0
		#nex=[]
		#for line in fin.readlines():
		#	#nex[nodes_inverse[int(c_n1)]]={}
		#	tmp=array.array("I")
		#	line=line.rstrip()[1:]
		#	dat=line.split(",")
		#	c_n2=0
		#	for x in dat:
		#		n,d=x.split("-")
		#		if c_n2==c_n1:
		#			tmp.append(int(0))
		#			c_n2=c_n2+1
		#			continue
		#		tmp.append(int(d))
		#		#nex[nodes_inverse[int(c_n1)]][nodes_inverse[int(c_n2)]]=nodes_inverse[)]
		#		c_n2=c_n2+1
		#	nex.append(tmp)
		#	c_n1=c_n1+1
		#	print "nex="+str(c_n1)
		#fin.close()
		#self.nex=nex
		##pickle.dump(nex,open("nex.pic","wb"))
		print "dne"
			

	#Load all the files.
	def load(self):
		fout1=open("emaps.csv","r")
		self.nodes_map={}
		self.nodes_inv={}
		for line in fout1.readlines():
			line=line.rstrip()
			print line
			nid,new = line.split(";")
			self.nodes_map[nid]=int(new)
			self.nodes_inv[int(new)]=nid
		fout1.close()
		fin=open("dataout-nex.csv","r")
		c_n1=0
		nex=[]
		for line in fin.readlines():
			#nex[nodes_inverse[int(c_n1)]]={}
			tmp=array.array("I")
			line=line.rstrip()[1:]
			dat=line.split(",")
			c_n2=0
			for x in dat:
				n,d=x.split("-")
				if c_n2==c_n1:
					tmp.append(int(0))
					c_n2=c_n2+1
					continue
				tmp.append(int(d))
				#nex[nodes_inverse[int(c_n1)]][nodes_inverse[int(c_n2)]]=nodes_inverse[)]
				c_n2=c_n2+1
			nex.append(tmp)
			c_n1=c_n1+1
			print "nex="+str(c_n1)
		fin.close()
		self.nex=nex
	
	#findPath is used to find the ideal path between two nodes.
	#distance is easy: self.dist[u][v]
	#Pass in two node IDs.
	def findPath(self,u,v):
		acndu=self.nodes_map[u]
		acndv=self.nodes_map[v]

		if self.nex[acndu][acndv]==None:
			return []
		path = [u]
		while acndu != acndv:
			acndu=self.nex[acndu][acndv]
			path.append(self.nodes_inv[acndu])
		return path