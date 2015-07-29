from qhull_2d import *
from min_bounding_rect import *
from LatLon import LatLon
import xml.etree.ElementTree as ET
class osm:
	filename=""
	root=None
	nodes={}
	ngraph=[]
	edges=[]
	paths=[]
	# Takes the filename for OpenStreetMaps XML.
	def __init__(self,filename):
		self.filename=filename
	#Open the file. Doesn't need to be called manually.
	def open(self):
		tree = ET.parse(self.filename)
		self.root = tree.getroot()
	#Runs all the data-gathering methods.
	#TODO: get a list of all buildings somewhere.
	def runAll(self):
		if self.root==None:
			self.open()
		self.collectNodes()
		self.getBuilding("Engineering 3")
		self.collectPaths()

	#Get all nodes using XPath from the OSM data.
	def collectNodes(self):
		for node in self.root.findall(".//node"):
			self.nodes[node.get("id")]=[float(node.get("lat")),float(node.get("lon"))]
	#Get the center-point for any given building.
	def getBuilding(self,name):
		points=[]
		for node in self.root.findall('.//way/tag[@v="'+name+'"]/../nd'): # Find Eng3 and get boundary points
			points.append(self.nodes[node.get("ref")])
		#Calculate a bounding box
		xy_points = array(points)
		hull_points = qhull2D(xy_points)
		hull_points = hull_points[::-1]
		(rot_angle, area, width, height, center_point, corner_points) = minBoundingRect(hull_points)
		self.ngraph.append({"id":"b-"+name,"coords":[center_point[0],center_point[1]],"ll":LatLon(center_point[0],center_point[1]),"neighbours":[]})
		
	#Collect all of the paths between buildings and around campus.
	def collectPaths(self):
		for node in self.root.findall('.//way/tag[@v="path"]/..')+self.root.findall('.//way/tag[@v="footway"]/..'):
			path=[]
			lnode=None
			for point in node.findall("nd"):
				path.append({"id":point.get("ref"),"coords":self.nodes[point.get("ref")]})
				node={"id":point.get("ref"),"coords":self.nodes[point.get("ref")],"ll":LatLon(self.nodes[point.get("ref")][0],self.nodes[point.get("ref")][1]),"neighbours":[]}
				if lnode != None:
					node["neighbours"].append(self.ngraph[-1]["id"])
					self.ngraph[-1]["neighbours"].append(node["id"])
					dist=node["ll"].distance(lnode["ll"])*1000
					dist=int(dist)# Don't need sub-meter accuracy, really.
					self.edges.append([node["id"],self.ngraph[-1]["id"],dist])
					self.edges.append([self.ngraph[-1]["id"],node["id"],dist])
				else:
					lnode=node
				self.ngraph.append(node)
			self.paths.append({"id":node.get("id"),"nodes":path})