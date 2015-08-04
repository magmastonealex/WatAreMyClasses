from jinja2 import Environment, PackageLoader
from db import Database
from model import WaterlooClassTime,WebNode
from services import Paths
import web
import json
"""
Temporary Index servlet to prove the concept.
Shows a map with a generated path.
"""

class PathAPIServlet:
	def GET(self):
		dbase=Database()
		pt = Paths(dbase)
		
		user_data = web.input(node1="b-E3",node2="b-E3")
		
		pth=[]
		for el in pt.getPath(user_data["node1"],user_data["node2"]):
			node=dbase.getNode(el)
			pth.append([node.id,node.x,node.y])

		return json.dumps({"path":pth})