from jinja2 import Environment, PackageLoader
from db import Database
from model import WaterlooClassTime,WebNode
from services import Paths
import web
import datetime

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
		
		classes=dbase.getDayClasses("")
		for cls in classes:
			x=classes.index(cls)
			if x ==0:
				classes[x].lastClassLoc="b-E3"
			else:
				classes[x].lastClassLoc=classes[x-1].build
			classes[x].class_name=classes[x].class_name.split(" - ")[0]
			classes[x].build="b-"+cls.where.split(" ")[0]
			classes[x].timestamp=classes[x].timestamp.strftime("%I:%M %p")
			classes[x].timeend=classes[x].timeend.strftime("%I:%M %p")
			if cls.type=="LEC":
				classes[x].col="warning"
			elif cls.type=="TST":
				classes[x].col="danger"
			elif cls.type=="TUT":
				classes[x].col="info"
			elif cls.type=="LAB":
				classes[x].col="success"
			elif cls.type=="SEM":
				classes[x].col="warning"




		xs=[]
		pth=[]
		for el in pt.getPath(nd1,"b-E3"):
			node=dbase.getNode(el)
			pth.append([node.x,node.y])
			xs.append(node)
		return template.render(vertices=xs,path=pth,classes=classes)