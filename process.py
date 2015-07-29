import xml.etree.ElementTree as ET
from numpy import *
from qhull_2d import *
from min_bounding_rect import *
from LatLon import LatLon
from Queue import Queue
from threading import Thread
import pickle
import os

INF=10**10

def floydwarshall(V, edges): #number of edges,
	#dist=[[INF]*V for i in range(V)]
	dist={}
	#init dist dictionary. I'm pretty sure that this will have the side effect of removing any dupes.
	for edge in edges:
		dist[edge[0]]={}
		for ed in edges:
			if ed[0] != edge[0]:
				dist[edge[0]][ed[0]]=INF
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
	#Return all the distances. NOT PATHS.
	return dist



tree = ET.parse('mapdata.xml')
root = tree.getroot()

#Dictionary of IDs to coords
nodes={}

# Get all nodes
for node in root.findall(".//node"):
	nodes[node.get("id")]=[float(node.get("lat")),float(node.get("lon"))]


points=[]
for node in root.findall('.//way/tag[@v="Engineering 3"]/../nd'): # Find Eng3 and get boundary points
	points.append(nodes[node.get("ref")])

#Calculate a bounding box
xy_points = array(points)
hull_points = qhull2D(xy_points)
hull_points = hull_points[::-1]

(rot_angle, area, width, height, center_point, corner_points) = minBoundingRect(hull_points)
print "Bounding Box of Eng3:"
print corner_points


#ngraph is all nodes. It will need some processing to figure out the path it came from.
ngraph=[]
ngraph.append({"id":"b-eng3","coords":[center_point[0],center_point[1]],"ll":LatLon(center_point[0],center_point[1]),"neighbours":[]}) # Get it out of numpy.

edges=[]
#Get paths and associated points
paths=[]
for node in root.findall('.//way/tag[@v="path"]/..')+root.findall('.//way/tag[@v="footway"]/..'):
	path=[]
	lnode=None
	for point in node.findall("nd"):
		path.append({"id":point.get("ref"),"coords":nodes[point.get("ref")]})
		node={"id":point.get("ref"),"coords":nodes[point.get("ref")],"ll":LatLon(nodes[point.get("ref")][0],nodes[point.get("ref")][1]),"neighbours":[]}
		if lnode != None:
			node["neighbours"].append(ngraph[-1]["id"])
			ngraph[-1]["neighbours"].append(node["id"])
			dist=dist=node["ll"].distance(lnode["ll"])*1000
			dist=int(dist)# Don't need sub-meter accuracy, really.
			edges.append([node["id"],ngraph[-1]["id"],dist])
			edges.append([ngraph[-1]["id"],node["id"],dist])
		else:
			lnode=node
		ngraph.append(node)
	paths.append({"id":node.get("id"),"nodes":path})
print len(ngraph)



#Rather inefficient. Runs in a bit less than O(n^2).

#Thread it? Yep

q = Queue()

cur=0
def checkNode():
	global q
	global cur
	global edges
	global ngraph
	while True:
		node,idx=q.get()
		nLL=node["ll"]
		for node2 in ngraph:
			if node["id"] == node2["id"] or node2["id"] in node["neighbours"]:
				continue
			n2LL=node2["ll"]
			dist=nLL.distance(n2LL)*1000 #distance in km, conv to m
			dist=int(dist) # Don't need sub-meter accuracy, really.
			if dist < 40:
				edges.append([node["id"],node2["id"],dist])
				ngraph[idx]["neighbours"].append(node2["id"])
				node2["neighbours"].append(node["id"])
		q.task_done()

if not os.path.exists("graph.pic"):
	for i in range(10): # Roughly falloff point of performance bell-curve on an octacore.
	     t = Thread(target=checkNode)
	     t.daemon = True # otherwise we need to keep track of them all. Just let them die on leave.
	     t.start()
	
	for node in ngraph:
		q.put([node,ngraph.index(node)])
	q.join()
	
	for node in ngraph: #de-duplication
		ngraph[ngraph.index(node)]["neighbours"]=list(set(node["neighbours"]))
	pickle.dump(ngraph,open("graph.pic","wb"))
	pickle.dump(edges,open("edges.pic","wb"))
else:
	print "Loaded calculated values"
	ngraph=pickle.load(open("graph.pic","rb"))
	edges=pickle.load(open("edges.pic","rb"))


print ngraph
print str(len(paths))+" paths found"