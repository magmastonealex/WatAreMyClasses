from jinja2 import Environment, PackageLoader
from db import Database
from model import WaterlooClassTime,WebNode
from services import Paths
import web
import json
"""
First API endpoint! Call:
/getpath?node1=nd1&node2=nd2, where nd1 and nd2 are the two nodes you want to navigate between.
Returns a JSON dictionary with the path key, which contains an array of (nodeID,lat,long) sets.

"""

class PathAPIServlet:
	def GET(self):
		dbase=Database()
		pt = Paths(dbase)
		
		user_data = web.input(node1="b-E3",node2="b-E3")
		
		pth=[]
		for el in pt.getPath(user_data["node1"],user_data["node2"]):
			node=dbase.getNode(el)
			pth.append({"id":node.id,"lat":node.x,"lon":node.y,"name":node.name})

		return json.dumps(pth)