import xml.etree.ElementTree as ET
from numpy import *

from qhull_2d import *
from min_bounding_rect import *

tree = ET.parse('mapdata.xml')
root = tree.getroot()
nodes={}
# Get all nodes
for node in root.findall(".//node"):
	nodes[node.get("id")]=[float(node.get("lat")),float(node.get("lon"))]

#Bounding box start

points=[]
for node in root.findall('.//way/tag[@v="Engineering 3"]/../nd'): # Find Eng3 and get points
	points.append(nodes[node.get("ref")])

#Calculate a bounding box
xy_points = array(points)

hull_points = qhull2D(xy_points)

hull_points = hull_points[::-1]

(rot_angle, area, width, height, center_point, corner_points) = minBoundingRect(hull_points)
print "Bounding Box of Eng3:"
#ngraph is all nodes. It will need some back-processing to figure out the path it came from. That's up next!
ngraph=[]
ngraph.append({"id":"b-eng3","coords":[center_point[0],center_point[1]]}) # Get it out of numpy.
print corner_points


#Get paths + points
paths=[]
for node in root.findall('.//way/tag[@v="path"]/..')+root.findall('.//way/tag[@v="footway"]/..'):
	path=[]
	for point in node.findall("nd"):
		path.append({"id":point.get("ref"),"coords":nodes[point.get("ref")]})
		ngraph.append({"id":point.get("ref"),"coords":nodes[point.get("ref")]})
	paths.append({"id":node.get("id"),"nodes":path})




print str(len(paths))+" paths found"