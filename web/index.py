from jinja2 import Environment, PackageLoader
from db import Database
from model import WaterlooClassTime,WebNode
from services import Paths
import web
"""
Temporary Index servlet to prove the concept.
Shows a map with a generated path.
"""

class IndexServlet:
	def GET(self):
		dbase=Database()

		user_data = web.input(node="2016012246")
		nd1=user_data.node
		
		pt = Paths(dbase)
		env = Environment(loader=PackageLoader('html', ''))
		template = env.get_template('maptest.html')
		

		xs=[]
		pth=[]
		for el in pt.getPath(nd1,"b-Engineering 3"):
			node=dbase.getNode(el)
			pth.append([node.x,node.y])
			xs.append(node)
		return template.render(vertices=xs,path=pth)