import xml.etree.ElementTree as ET
from numpy import *
from qhull_2d import *
from min_bounding_rect import *

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
ngraph.append({"id":"b-eng3","coords":[center_point[0],center_point[1]]}) # Get it out of numpy.



#Get paths and associated points
paths=[]
for node in root.findall('.//way/tag[@v="path"]/..')+root.findall('.//way/tag[@v="footway"]/..'):
	path=[]
	for point in node.findall("nd"):
		path.append({"id":point.get("ref"),"coords":nodes[point.get("ref")]})
		ngraph.append({"id":point.get("ref"),"coords":nodes[point.get("ref")]})
	paths.append({"id":node.get("id"),"nodes":path})

print str(len(paths))+" paths found"