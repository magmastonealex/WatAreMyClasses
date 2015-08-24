from calc.qhull_2d import *
from calc.min_bounding_rect import *
from LatLon import LatLon
import xml.etree.ElementTree as ET
from viewer import NodeCollection,Node
"""
Scrapes data from an OpenStreetMaps XML file.

Usage:

x=osm("mapdata2.xml",nodeCollection)
x.runAll(buildingList). - Uses a dictionary as returned by the buildingList parser.

It will attempt to search for the buildings in lots of different ways. 

nodeCollection now is populated with data.

May want to consider adding hallways for truly shortest path, but also causes strange pathfinding problems.
"""
class osm:
	filename=""
	root=None
	bL=None
	paths=[]
	nCollection=None
	# Takes the filename for OpenStreetMaps XML.
	def __init__(self,filename,nodeCollection):
		self.filename=filename

		self.nCollection=nodeCollection
	#Open the file. Doesn't need to be called manually.
	def open(self):
		tree = ET.parse(self.filename)
		self.root = tree.getroot()
	#Runs all the data-gathering methods.
	#TODO: get a list of all buildings somewhere.
	def runAll(self,buildings):
		if self.root==None:
			self.open()
		self.collectNodes()
		for sf,building in buildings.items():
			self.getBuilding(building,sf)
		self.collectPaths()
	tempNodes={}
	#Get all nodes using XPath from the OSM data. This isn't in usual node format because we don't know or care about neighbours/relative nodes. at this point.
	def collectNodes(self):
		for node in self.root.findall(".//node"):	
			self.tempNodes[node.get("id")]=[float(node.get("lat")),float(node.get("lon"))]

	#Get the center-point for any given building.
	def getBuilding(self,name,shortnm):
		points=[]

		for node in self.root.findall('.//way/tag[@v="'+name.replace("'","\'").replace("&","&amp;")+'"]/../nd'): # Find Eng3 and get boundary points
			points.append(self.tempNodes[node.get("ref")])
		if len(points)==0:
			for node in self.root.findall('.//way/tag[@v="'+shortnm+'"]/../nd'): # Find Eng3 and get boundary points
				points.append(self.tempNodes[node.get("ref")])
			if len(points)==0:
				for node in self.root.findall('.//relation/tag[@v="'+name.replace("'","\'").replace("&","&amp;")+'"]/../member[@type="node"]'): # Find Eng3 and get boundary points
					points.append(self.tempNodes[node.get("ref")])
				if len(points)==0:
					for node in self.root.findall('.//relation/tag[@v="'+shortnm+'"]/../member[@type="node"]'): # Find Eng3 and get boundary points
						points.append(self.tempNodes[node.get("ref")])
					if len(points)==0:
						for node in self.root.findall('.//relation/tag[@v="'+name.replace("'","\'").replace("&","&amp;")+'"]/../nd'): # Find Eng3 and get boundary points
							points.append(self.tempNodes[node.get("ref")])
						if len(points)==0:
							for node in self.root.findall('.//relation/tag[@v="'+shortnm+'"]/../nd'): # Find Eng3 and get boundary points
								points.append(self.tempNodes[node.get("ref")])
							if len(points)==0:
								if name.find("Columbia Lake") ==-1 and name.find("Ron Eydt") == -1 and name.find("UW Place") == -1 and name.find("V1") == -1 and name.find("Village 1") == -1:
									print name +" - not found!"
								return
#		else:
#			print name + " - found!"
		#Calculate a bounding box
		xy_points = array(points)
		hull_points = qhull2D(xy_points)
		hull_points = hull_points[::-1]
		(rot_angle, area, width, height, center_point, corner_points) = minBoundingRect(hull_points)
		self.nCollection.addNode("b-"+shortnm,center_point[0],center_point[1],name=name,latlong=LatLon(center_point[0],center_point[1]))
		
	#Collect all of the paths between buildings and around campus.
	def collectPaths(self):
		for node in self.root.findall('.//way/tag[@v="path"]/..')+self.root.findall('.//way/tag[@v="footway"]/..')+self.root.findall('.//way/tag[@v="tertiary"]/..')+self.root.findall('.//way/tag[@v="service"]/..'): #+self.root.findall('.//way/tag[@v="corridor"]/..'): # these are hallways.
			path=[]
			lnode=None
			for point in node.findall("nd"):
				path.append(point.get("ref"))

				self.nCollection.addNode(point.get("ref"),self.tempNodes[point.get("ref")][0],self.tempNodes[point.get("ref")][1],latlong=LatLon(self.tempNodes[point.get("ref")][0],self.tempNodes[point.get("ref")][1]))
				if lnode != None:
					dist=self.nCollection[point.get("ref")].latlong.distance(self.nCollection[lnode].latlong)*1000
					dist=int(dist)# Don't need sub-meter accuracy, really.
					self.nCollection.addEdge(point.get("ref"),lnode,dist)
					#print lnode+"-"+point.get("ref")
				lnode=point.get("ref")

			self.paths.append({"id":node.get("id"),"nodes":path})
