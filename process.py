import xml.etree.ElementTree as ET
from numpy import *
from qhull_2d import *
from min_bounding_rect import *
from LatLon import LatLon
from Queue import Queue
from threading import Thread

INF=10**10

def floydwarshall(V, edges): #number of edges,
	dist=[[INF]*V for i in range(V)]

	for i in range(V):
		dist[i][i] = 0
	
	for (start,end,distance) in edges:
		dist[start][end] = distance

	for k in range(V):
		for j in range(V):
			for i in range(V):
				if dist[i][j] > dist[i][k] + dist[k][j]:
					dist[i][j] = dist[i][k] + dist[k][j]

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
		else:
			lnode=node
		ngraph.append(node)
	paths.append({"id":node.get("id"),"nodes":path})
print len(ngraph)


#Inefficient to a ridiculous degree. Better way of doing this?
#Probably want to pickle/otherwise save this.
#Also not sure if we want to use LatLon for this. 
#Great-circle distances are an alternative, but LatLong uses that under the hood anyways.
#LatLong also offers headings between points and other simplified geo-calculations.

#Thread it? Yep

q = Queue()
edges=[]
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
			if node["id"] == node2["id"]:
				continue
			n2LL=node2["ll"]
			dist=nLL.distance(n2LL)*1000
			if (dist) < 80: #distance in km, conv to m
				
				edges.append([node2["id"],node["id"],dist])
				edges.append([node["id"],node2["id"],dist])
	
				ngraph[idx]["neighbours"].append(node2["id"])
				node2["neighbours"].append(node["id"])
		q.task_done()

for i in range(10): # Roughly falloff point of performance bell-curve on an octacore.
     t = Thread(target=checkNode)
     t.daemon = True # otherwise we need to keep track of them all. Just let them die on leave.
     t.start()

for node in ngraph:
	q.put([node,ngraph.index(node)])
q.join()

#Get rid of non-unique neighbours
for node in ngraph:
	node["neighbours"]=list(set(node["neighbours"]))
print ngraph
print str(len(paths))+" paths found"