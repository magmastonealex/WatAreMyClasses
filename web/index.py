from jinja2 import Environment, PackageLoader
from viewer import NodeCollection,Node
from services import Paths


class IndexServlet:
	def GET(self):
		user_data = web.input(node="2016012246")
		nd1=user_data.node
		
		print "Hi"
		pt = Paths()
		env = Environment(loader=PackageLoader('html', ''))
		template = env.get_template('maptest.html')
		nC=NodeCollection()
		nC.load()
		
		xs=[]
		
		pth=[]
		
		for el in pt.getPath(nd1,"b-Engineering 3"):
			pth.append([nC[el].x,nC[el].y])
			xs.append(nC[el])
		
		
		return template.render(vertices=xs,path=pth)