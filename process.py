import xml.etree.ElementTree as ET
from numpy import *

from qhull_2d import *
from min_bounding_rect import *

tree = ET.parse('mapdata.xml')
root = tree.getroot()
nodes={}

for node in root.findall(".//node"):
	nodes[node.get("id")]=[float(node.get("lat")),float(node.get("lon"))] # Watch out for this. Longitudes are all +ve numbers. Switch before displaying!
points=[]
for node in root.findall('.//way/tag[@v="Engineering 3"]/../nd'): # Find Eng3 and get a bounding box
	points.append(nodes[node.get("ref")])

xy_points = array(points)

hull_points = qhull2D(xy_points)

hull_points = hull_points[::-1]

(rot_angle, area, width, height, center_point, corner_points) = minBoundingRect(hull_points)
print "Bounding Box of Eng3:"
print corner_points

paths=[]
for node in root.findall('.//way/tag[@v="path"]/..')+root.findall('.//way/tag[@v="footway"]/..'):
	path=[]
	for point in node.findall("nd"):
		path.append(nodes[point.get("ref")])
	paths.append(path)

print str(len(paths))+" paths found"